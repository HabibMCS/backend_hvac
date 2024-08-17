from utility import HVACSystem
import env
import requests
import pandas as pd
import sys
import COP

def csv_download(outfile, hvac, parameter_mapping, date, start, end, token, system_uri, unit_uri):
    output_csv_file = outfile
    
    # Cache system and unit information
    system_json, units_json = hvac.get_unitandsystem(token=token, uri=unit_uri)
    
    if not system_json:
        print("No system data retrieved.")
        return
    
    system_ids = list(system_json.keys())
    print(system_ids)
    
    # Get timestamp range once
    start_timestamp_ms, end_timestamp_ms = hvac.get_time_range_timestamps(date, start_hour=start, end_hour=end)
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

def main():
    outfile = 'Updated_system.csv'
    
    # # Download and process data
    # try:
    #     csv_download(outfile=outfile, hvac=HVACSystem(), parameter_mapping=env.parameters_mapping, 
    #              date= "27/07/2024", start=9, end=17, 
    #              token=env.token, system_uri=env.system_uri, unit_uri=env.unit_uri)
    # except Exception as e:
    #     print(e)

    # df = pd.read_csv(outfile)
    # df = df.dropna(axis=1, how='all')
    
    # df.to_csv(outfile, index=False)

    print(f"Processed data and saved cleaned CSV to {outfile}.")

    total_data_count,data_count_more_10_percent,data_count_less_10_percent,percent_within_10_percent = COP.COP(outfile= outfile, sample_time = "5T")
    print(f'Total Data Count: {total_data_count}')
    print(f'Data Count > 10% error: {data_count_more_10_percent}')
    print(f'Data Count < -10% error: {data_count_less_10_percent}')

    print(f'Percentage of energy balance within 10% : {percent_within_10_percent}%')

if __name__ == "__main__":
    main()
