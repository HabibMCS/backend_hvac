import json
import csv
from datetime import datetime
import requests
import pytz


class HVACSystem:
    def __init__(self) -> None:
        pass
    def getparams(self,uri,token):
        headers = {'x-access-token': token}
        parameters = {}
        try:
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
            print(response.encoding)  # Check the detected encoding
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {}, {}
        for key,values in data["data"].items():
            parameters[key]=values.get("title")
        return parameters

    def get_unitandsystem(self, token, uri):
        headers = {'x-access-token': token}

        try:
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return {}, {}

        systems_data = {}
        mapped_data = {}

        for key, value in data["data"].items():
            name = value["name"]

            # Mapping systems
            system_number = value.get("systemNumber")
            system = value.get("system")
            if system_number and system:
                systems_data[system] = system_number

            # Mapping units
            control_id = value.get("controlUnit")
            if control_id and control_id in data["data"]:
                associated_name = data["data"][control_id]["name"]
                mapped_data[key] = associated_name

            if name.startswith("ODU"):
                mapped_data[key] = name

        return systems_data, mapped_data

    @staticmethod
    def read_json_from_file(filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file {filename}: {e}")
            return {}

    def map_entries(self, entries, parameter_mapping, unit_id, unit_type, unit_name_mapping):
        tz = pytz.timezone('Asia/Singapore')
        unit_name = unit_name_mapping.get(unit_id, unit_id)

        mapped_entries = []
        for entry in entries:
            timestamp = datetime.fromtimestamp(entry['timestamp'] / 1000, tz)
            mapped_entry = {
                "Time Stamp": timestamp.strftime('%d/%m/%y %H:%M'),
                "Unit Name": unit_name,
                "Unit Type": unit_type
            }
            mapped_entry.update({
                parameter_mapping.get(str(k), k): v for k, v in entry.items() if k != 'timestamp'
            })
            mapped_entries.append(mapped_entry)
        return mapped_entries

    def process_json(self, json_data, parameter_mapping, unit_name_mapping):
        all_entries = []

        for unit_type in ["indoors", "outdoors"]:
            units = json_data.get("data", {}).get(unit_type, {})
            for unit_id, unit_data in units.items():
                entries = unit_data.get("entries", [])
                mapped_entries = self.map_entries(entries, parameter_mapping, unit_id, unit_type, unit_name_mapping)
                all_entries.extend(mapped_entries)

        return all_entries

    def write_to_csv(self, mapped_entries, parameter_mapping, output_file):
        fieldnames = ["Time Stamp", "Unit Name", "Unit Type"] + list(parameter_mapping.values())

        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            for entry in mapped_entries:
                complete_entry = {key: entry.get(key, '') for key in fieldnames}
                writer.writerow(complete_entry)

    @staticmethod
    def get_time_range_timestamps(date_str, date_format="%d/%m/%Y", start_hour=9, end_hour=17, timezone="Asia/Singapore"):
        tz = pytz.timezone(timezone)
        date = datetime.strptime(date_str, date_format)

        start_time = tz.localize(datetime(date.year, date.month, date.day, start_hour, 0, 0))
        end_time = tz.localize(datetime(date.year, date.month, date.day, end_hour, 0, 0))

        start_timestamp_ms = int(start_time.timestamp() * 1000)
        end_timestamp_ms = int(end_time.timestamp() * 1000)

        return start_timestamp_ms, end_timestamp_ms
