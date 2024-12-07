from flask import Flask, request, jsonify, send_file  # Standard library (third-party)
from flask_cors import CORS  # Third-party
import os  # Standard library
from datetime import datetime  # Standard library
import concurrent.futures  # Standard library
import requests  # Third-party
import pandas as pd  # Third-party
from utility import HVACSystem
# from calculateCOP import perform_calculations
# from transform_data import process_csv_and_filter 
# from calculateCOP import calculate_COP_from_df
import env


app = Flask(__name__)
CORS(app)
hvac = HVACSystem()
df_reduced = pd.read_csv('./data/reduced.csv')
df_all_sys_res = pd.read_csv('./data/Allsystemsresultssummary.csv')

# Function to download system data (adapted from your code)
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

def indexprocess(csv_file):
    try:
        # Process the CSV and filter data between start_date and end_date
        # systems_data = process_csv_and_filter(csv_file, start_date, end_date)
        
        # Initialize a dictionary to hold the JSON representations of each system's data
        # system_data_json = {}
        
        # Iterate over systems in systems_data dynamically
        # for system_name, system_df in systems_data.items():
            # Calculate COP for the current system
        system_df = pd.read_csv(csv_file)
        
# Convert 'Time Stamp' to datetime with dayfirst=True
        system_df['Time Stamp'] = pd.to_datetime(system_df['Time Stamp'], format="%d/%m/%y %H:%M", dayfirst=True)

        # Further filter the DataFrame to include only times between 9 AM and 5 PM
        df_filtered = system_df[system_df['Time Stamp'].dt.hour.between(9, 17)]

    
        cop_values_raw, timestamp= perform_calculations(df_filtered)
            
        # Check if cop_values_raw is a DataFrame
        if isinstance(cop_values_raw, pd.DataFrame):
            cop_values = cop_values_raw.tolist()  # Convert to list
        else:
            # Handle scalar value case
            cop_values = [cop_values_raw]  # Wrap in a list

        # Assuming timestamp is already a DataFrame or Series
        # Convert timestamp to a list
        timestamp = timestamp.tolist()  

        # Add the system data and COP values to the dictionary in JSON format
        system_data_json = {
            "timestamp": timestamp,
            "cop_values": cop_values
        }

        # return system_data_json

    except Exception as e:
        print(f"Error processing data: {e}")
        return {"error": f"Error processing data: {e}"}, 500

    # Return the dynamic dictionary containing JSON data for all systems
    return system_data_json


# Endpoint to trigger CSV download
@app.route('/download_csv', methods=['POST'])
def download_csv():
    data = request.json
    token = data.get('token')
    system_number = data.get('system_number')
    # date = data.get('date')
    # date2 = data.get('date2', None)

    if not token or system_number is None:
        return jsonify({"error": "Invalid input parameters"}), 400

    # Convert date to datetime
    # try:
    #     date_obj = datetime.strptime(date, '%Y-%m-%d')
    #     if date2:
    #         date2_obj = datetime.strptime(date2, '%Y-%m-%d')
    #     else:
    #         date2_obj = None
    # except ValueError:
    #     return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD"}), 400

    output_dir = './outputs/individual_systems'
    os.makedirs(output_dir, exist_ok=True)

    # Cache system and unit information
    # system_json, units_json = hvac.get_unitandsystem(token=token, uri=env.unit_uri)

    # if not system_json:
    #     return jsonify({"error": "No system data retrieved"}), 500

    # system_ids = list(system_json.keys())
    # system_id = system_ids[system_number]
    # parameter_mapping = hvac.getparams(uri=env.service_uri, token=token)

    # if date2:
    #     segments = hvac.get_segments(date, date2)  # Generate segments between date and date2
    # else:
    #     start_timestamp_ms, end_timestamp_ms = hvac.get_time_range_timestamps(date)
    #     segments = [(start_timestamp_ms, end_timestamp_ms)]  # Single segment if no date2 provided

    # individual_csv_files = []

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_to_system = {
    #         executor.submit(download_system_data, system_id, hvac, token, env.system_uri, env.service_uri, units_json, parameter_mapping, segments, output_dir): system_id
    #     }

    #     for future in concurrent.futures.as_completed(future_to_system):
    #         try:
    #             system_csv_file = future.result()
    #             individual_csv_files.append(system_csv_file)
    #         except Exception as e:
    #             return jsonify({"error": f"Error processing system {system_id}: {e}"}), 500

    # Return the CSV file to the frontend
    try:
        csv_file_path = "./results.csv" # For simplicity, let's assume we return the first one
        final_json_data = indexprocess(csv_file_path)
        return final_json_data
    except:
        return jsonify({"error": "No data to download"}), 500

@app.route('/get_time', methods=['GET'])
def get_time():
    return jsonify(df_reduced.iloc[:, 0].tolist())

@app.route('/get_cop', methods=['GET'])
def get_cop():
    return jsonify(df_reduced.iloc[:, 1].tolist())

@app.route('/get_cooling', methods=['GET'])
def get_cooling():
    return jsonify(df_reduced.iloc[:, 2].tolist())


if __name__ == '__main__':
    app.run(debug=True)
