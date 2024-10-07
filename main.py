'''SCRIPT IN DEVELOPMENT DO NOT RUN, USE SANDBOX SCRIPT'''

import concurrent.futures
import os
import requests
import pandas as pd
import schedule
import time
from datetime import datetime
from utility import HVACSystem
import subprocess , sys
import env
from transform_data import data_transform_and_split

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
                print("done")
            else:
                print(f"No data received for system {system_id} for segment {segment_start} to {segment_end}")

        except requests.exceptions.RequestException as e:
            print(f"Request error for system {system_id} for segment {segment_start} to {segment_end}: {e}")
            continue

    # Write data to the individual system CSV
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

    # Combine all individual CSVs into one final CSV
    combined_df = pd.concat([pd.read_csv(csv_file, encoding='utf-8') for csv_file in individual_csv_files])
    combined_df = combined_df.dropna(axis=1, how='all')
    combined_df.to_csv(outfile, index=False, encoding='utf-8')

    print(f"Processed data and saved combined CSV to {outfile}.")

def download_and_process_data():
    # Define the output file path with today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    outfile = f'./outputs/data_{today_date}.csv'
    
    # Download and process data
    try:
        date = "25/04/2024"
        csv_download(outfile=outfile, hvac=HVACSystem(), date=date,
                     token=env.token, system_uri=env.system_uri, unit_uri=env.unit_uri, service_uri=env.service_uri)
        
        # Load the downloaded CSV, remove empty columns, and save it
        df = pd.read_csv(outfile)
        df.dropna(axis=1, how='all', inplace=True)  # Drop columns that are entirely empty
        df.dropna( how='all')
        df.to_csv(outfile, index=False)  # Save the cleaned DataFrame back to the CSV
        data_transform_and_split(df,date)
        # run the local file calculatecop.py with current python env
        subprocess.run([sys.executable, 'calculatecop.py'], check=True)
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    # Schedule the data download and processing for every day at 11 PM
    schedule.every().day.at("23:00").do(download_and_process_data)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    pass #  main()
