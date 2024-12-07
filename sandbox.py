import concurrent.futures
import os
import requests
import pandas as pd
import subprocess
import sys
import env
from datetime import datetime, timedelta
from utility import HVACSystem
from transform_data import data_transform_and_split
from calculation_summary_uncertainity import calculate_uncertainity_summary
from google.cloud import storage  # Import Google Cloud Storage library

def upload_to_gcp(bucket_name, source_file, destination_blob):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(source_file)
    print(f"Uploaded {source_file} to {destination_blob} in bucket {bucket_name}.")

def download_system_data(system_id, hvac, token, system_uri, service_uri, units_json, parameter_mapping, segments, output_dir):
    headers = {'x-access-token': token}
    url = f"{system_uri}{system_id}"
    system_csv_file = os.path.join(output_dir, f'system_{system_id}.csv')
    all_mapped_entries = []

    for segment_start, segment_end in segments:
        start_timestamp_ms = int(segment_start.timestamp() * 1000)
        end_timestamp_ms = int(segment_end.timestamp() * 1000)
        params = {
            'startTimeUTC': start_timestamp_ms,
            'endTimeUTC': end_timestamp_ms
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            json_input = response.json()

            if json_input:
                mapped_entries = hvac.process_json(json_data=json_input, parameter_mapping=parameter_mapping, unit_name_mapping=units_json)
                all_mapped_entries.extend(mapped_entries)
                print(f"Data retrieved for system {system_id} for segment {segment_start} to {segment_end}.")
            else:
                print(f"No data received for system {system_id} for segment {segment_start} to {segment_end}")

        except requests.exceptions.RequestException as e:
            print(f"Request error for system {system_id} for segment {segment_start} to {segment_end}: {e}")
            continue

    if all_mapped_entries:
        hvac.write_to_csv(all_mapped_entries, parameter_mapping, system_csv_file)

    return system_csv_file

def csv_download(outfile, hvac, date, token, system_uri, unit_uri, service_uri, date2=None):
    output_dir = './outputs/individual_systems'
    os.makedirs(output_dir, exist_ok=True)
    
    # Cache system and unit information
    system_json, units_json = hvac.get_unitandsystem(token=token, uri=unit_uri)
    
    if not system_json:
        print("No system data retrieved.")
        return
    
    system_ids = list(system_json.keys())
    parameter_mapping = hvac.getparams(uri=service_uri, token=token)

    if date2:
        segments = hvac.get_segments(date, date2)  # Generate segments between date and date2
    else:
        start_timestamp_ms, end_timestamp_ms = hvac.get_time_range_timestamps(date)
        segments = [(start_timestamp_ms, end_timestamp_ms)]  # Single segment if no date2 provided

    individual_csv_files = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_system = {executor.submit(download_system_data, system_id, hvac, token, system_uri, service_uri, units_json, parameter_mapping, segments, output_dir): system_id for system_id in system_ids}

        for future in concurrent.futures.as_completed(future_to_system):
            system_id = future_to_system[future]
            try:
                system_csv_file = future.result()
                individual_csv_files.append(system_csv_file)
            except Exception as e:
                print(f"Error processing system {system_id}: {e}")

    combined_df = pd.concat([pd.read_csv(csv_file, encoding='utf-8') for csv_file in individual_csv_files])
    combined_df = combined_df.dropna(axis=1, how='all')
    combined_df.to_csv(outfile, index=False, encoding='utf-8')

    print(f"Processed data and saved combined CSV to {outfile}.")

def download_and_process_data(date):
    """Downloads and processes data for the given date."""
    today_date = date.strftime("%Y-%m-%d")
    outfile = f'./outputs/data_{today_date}.csv'
    
    try:
        csv_download(outfile=outfile, hvac=HVACSystem(), date=today_date,
                     token=env.token, system_uri=env.system_uri, unit_uri=env.unit_uri, service_uri=env.service_uri)
        

        df = pd.read_csv(outfile)
        df.dropna(axis=1, how='all', inplace=True) 
        df.dropna(how='all', inplace=True)  
        df.to_csv(outfile, index=False)  
        
        data_transform_and_split(df, today_date)
        
        # Run the local file calculatecop.py with current python env
        subprocess.run([sys.executable, 'calculateCOP.py'], check=True)

        calculate_uncertainity_summary()

        prefix_files_with_date(today_date, outfile)
        
    except Exception as e:
        print(f"Error occurred: {e}")

def prefix_files_with_date(date, outfile):
    """Prefixes the individual system files with the specified date and uploads them to GCP."""
    transformed_dir = './outputs/Cleantransformeddatabeforecalculation'
    results_dir = './outputs/Resultswithoutliers'
    
    bucket_name = 'traindata4m'  
    new_filename = f"all_sys_{date}.csv"  

    uncern_file = f"./outputs/Uncertainitysummary/Allsystemsresultssummary.csv"
    upload_to_gcp(bucket_name, outfile, f"COPData/sitedata/{new_filename}")
    upload_to_gcp(bucket_name, uncern_file, f"COPData/uncertainity_summary/file_{date}.csv")

    for filename in os.listdir(transformed_dir):
        if filename.endswith('.csv'):
            new_filename = f"{date}_{filename}"
            upload_to_gcp(bucket_name, os.path.join(transformed_dir, filename), f"COPData/transformed/{new_filename}")

    for filename in os.listdir(results_dir):
        if filename.endswith('.csv'):
            new_filename = f"{date}_{filename}"
            upload_to_gcp(bucket_name, os.path.join(results_dir, filename), f"COPData/Results/{new_filename}")

    os.remove(outfile)  
    os.remove(uncern_file) 
    for filename in os.listdir(transformed_dir):
        os.remove(os.path.join(transformed_dir, filename))

    for filename in os.listdir(results_dir):
        os.remove(os.path.join(results_dir, filename))

def run_for_past_two_weeks():
    """Runs the download and processing for the last 14 days."""
    today = datetime.now()
    
    for i in range(14):
        date = today - timedelta(days=i)
        print(f"Processing data for {date.strftime('%Y-%m-%d')}")
        download_and_process_data(date)

def main():
    run_for_past_two_weeks()

if __name__ == "__main__":
    main()
