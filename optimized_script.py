import concurrent.futures
import os
import requests
import pandas as pd
import subprocess
import sys
import env
import gc
from datetime import datetime, timedelta
from utility import HVACSystem
from transform_data import data_transform_and_split
from calculation_summary_uncertainity import calculate_uncertainity_summary
from google.cloud import storage
import time
CREDENTIALS_PATH = "./creds.json"

def get_date_segments(start_date, end_date, days_per_chunk=2):
    current = start_date
    while current < end_date:
        segment_end = min(current + timedelta(days=days_per_chunk), end_date)
        yield current, segment_end
        current = segment_end

def download_system_data(system_id, hvac, token, system_uri, service_uri, units_json, 
                        parameter_mapping, segment_start, segment_end, output_dir):
    headers = {'x-access-token': token}
    url = f"{system_uri}{system_id}"
    system_csv_file = os.path.join(output_dir, f'system_{system_id}_{segment_start.strftime("%Y%m%d")}.csv')
    
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
            mapped_entries = hvac.process_json(json_input, parameter_mapping, units_json)
            if mapped_entries:
                pd.DataFrame(mapped_entries).to_csv(system_csv_file, index=False)
                print(f"Data saved for system {system_id}: {segment_start} to {segment_end}")
                return system_csv_file
    except Exception as e:
        print(f"Error for system {system_id}: {e}")
    return None

def process_segment(segment_start, segment_end, hvac, token, system_uri, unit_uri, service_uri):
    output_dir = './outputs/individual_systems'
    os.makedirs(output_dir, exist_ok=True)
    
    system_json, units_json = hvac.get_unitandsystem(token=token, uri=unit_uri)
    if not system_json:
        return []
    
    parameter_mapping = hvac.getparams(uri=service_uri, token=token)
    valid_files = []

    # Process systems in smaller batches
    system_ids = list(system_json.keys())
    batch_size = 5
    for i in range(0, len(system_ids), batch_size):
        batch_systems = system_ids[i:i + batch_size]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(
                    download_system_data, 
                    system_id, hvac, token, system_uri, service_uri,
                    units_json, parameter_mapping, segment_start, segment_end, output_dir
                ): system_id for system_id in batch_systems
            }
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        valid_files.append(result)
                except Exception as e:
                    print(f"Batch processing error: {e}")
        
        gc.collect()  # Force garbage collection between batches
    
    return valid_files

def process_and_upload_data(date, files, chunk_size=1000):
    date_str = date.strftime("%Y-%m-%d")
    outfile = f'./outputs/data_{date_str}.csv'
    
    # Process files in chunks
    with open(outfile, 'w') as out:
        first_chunk = True
        for file in files:
            for chunk in pd.read_csv(file, chunksize=chunk_size):
                if first_chunk:
                    chunk.to_csv(out, index=False)
                    first_chunk = False
                else:
                    chunk.to_csv(out, index=False, header=False)
            os.remove(file)
    
    # Process the combined file in chunks
    df = pd.read_csv(outfile)
    data_transform_and_split(df)
    subprocess.run([sys.executable, 'calculateCOP.py'], check=True)
    calculate_uncertainity_summary()
    
    # Upload to GCP
    bucket_name = 'traindata4m'
    client = setup_gcp_auth()
    bucket = client.bucket(bucket_name)
    
    for dir_path, gcp_prefix in [
        (outfile, f"COPData/sitedata/all_sys_{date_str}.csv"),
        (f"./outputs/Uncertainity summary/All systems results summary.csv", 
         f"COPData/uncertainity_summary/file_{date_str}.csv"),
        ('./outputs/Clean transformed data before calculation', 'COPData/transformed'),
        ('./outputs/Results with outliers', 'COPData/Results')
    ]:
        if isinstance(dir_path, str) and os.path.isdir(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith('.csv'):
                    local_path = os.path.join(dir_path, filename)
                    gcp_path = f"{gcp_prefix}/{date_str}_{filename}"
                    bucket.blob(gcp_path).upload_from_filename(local_path)
                    os.remove(local_path)
        elif os.path.isfile(dir_path):
            bucket.blob(gcp_prefix).upload_from_filename(dir_path)
            os.remove(dir_path)
def setup_gcp_auth():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
    return storage.Client()

def main():
#    storage_client = setup_gcp_auth()
    hvac = HVACSystem()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    # Process historical data in segments
    for segment_start, segment_end in get_date_segments(start_date, end_date):
        print(f"Processing segment: {segment_start} to {segment_end}")
        files = process_segment(
            segment_start, segment_end,
            hvac, env.token, env.system_uri, env.unit_uri, env.service_uri
        )
        if files:
            process_and_upload_data(segment_end, files)
        gc.collect()
    
    # Switch to daily processing
    while True:
        now = datetime.now()
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        time.sleep((next_run - now).total_seconds())
        
        yesterday = now - timedelta(days=1)
        files = process_segment(
            yesterday, now,
            hvac, env.token, env.system_uri, env.unit_uri, env.service_uri
        )
        if files:
            process_and_upload_data(yesterday, files)
        gc.collect()

if __name__ == "__main__":
    main()
