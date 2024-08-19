###############  git@github.com:HabibMCS/backend_hvac.git

from utility import HVACSystem
import env
import requests
import pandas as pd
import sys
import COP


def csv_download(outfile, hvac, date,token, system_uri, unit_uri,service_uri, date2 = None):
    output_csv_file = outfile
    
    # Cache system and unit information
    system_json, units_json = hvac.get_unitandsystem(token=token, uri=unit_uri)
    
    if not system_json:
        print("No system data retrieved.")
        return
    
    system_ids = list(system_json.keys())
    print(system_ids)
    parameter_mapping = hvac.getparams(uri = service_uri,token=token)
    
    # Get timestamp range once
    if date2 is None:
        start_timestamp_ms, end_timestamp_ms = hvac.get_time_range_timestamps(date)

        try:
            for system_id in system_ids:
                headers = {'x-access-token': token}
                url = f"{system_uri}{system_id}"

                params = {
                    'startTimeUTC': start_timestamp_ms,
                    'endTimeUTC': end_timestamp_ms
                }

                try:
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    json_input = response.json()
                except requests.exceptions.RequestException as e:
                    print(f"Request error for system {system_id}: {e}")
                    continue

                if json_input:
                    mapped_entries = hvac.process_json(json_data=json_input, parameter_mapping=parameter_mapping, unit_name_mapping = units_json)
                    hvac.write_to_csv(mapped_entries, parameter_mapping, output_csv_file)
                else:
                    print(f"No data received for system {system_id} on the specific date: {date}")
        except Exception as e:
            print(e)
    elif date2:
        try:
            for system_id in system_ids:
                segments = hvac.get_segments(date,date2)
                for segment_start, segment_end in segments:
                    start_timestamp_ms = int(segment_start.timestamp() * 1000)
                    end_timestamp_ms = int(segment_end.timestamp() * 1000)
                    url = f"{system_uri}{system_id}"
                    headers = {'x-access-token': token}

                    params = {
                        'startTimeUTC': start_timestamp_ms,
                        'endTimeUTC': end_timestamp_ms
                    }

                    try:
                        response = requests.get(url, headers=headers, params=params)
                        response.raise_for_status()  # Check for HTTP errors
                        json_input = response.json()
                    except requests.exceptions.RequestException as e:
                        print(f"Request error: {e}")
                        continue
                    if json_input:
                            mapped_entries = hvac.process_json(json_data=json_input, parameter_mapping=parameter_mapping, unit_name_mapping = units_json)
                            hvac.write_to_csv(mapped_entries, parameter_mapping, output_csv_file)
                            print("done")
                    else:
                            print(f"No data received for system {system_id} on the specific date: {date}")
        except Exception as e:
            print(e)




def main():
    outfile = './outputs/data_100724.csv'
    
    # Download and process data
    try:
        csv_download(outfile=outfile, hvac=HVACSystem() ,date= "10/07/2024",date2=None,
                 token=env.token, system_uri=env.system_uri, unit_uri=env.unit_uri,service_uri=env.service_uri)
    except Exception as e:
        print(e)

    df = pd.read_csv(outfile, encoding='utf-8')
    df = df.dropna(axis=1, how='all')
    
    df.to_csv(outfile, index=False,encoding='utf-8')

    print(f"Processed data and saved cleaned CSV to {outfile}.")
    with open("col.txt", "w+", encoding='utf-8') as file:
        file.write(','.join(f"'{col}'" for col in df.columns) + '\n')
    # total_data_count,data_count_more_10_percent,data_count_less_10_percent,percent_within_10_percent = COP.COP(outfile= outfile, sample_time = "5T")
    # print(f'Total Data Count: {total_data_count}')
    # print(f'Data Count > 10% error: {data_count_more_10_percent}')
    # print(f'Data Count < -10% error: {data_count_less_10_percent}')

    # print(f'Percentage of energy balance within 10% : {percent_within_10_percent}%')

if __name__ == "__main__":
    main()
