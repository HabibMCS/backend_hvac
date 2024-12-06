
import CoolProp.CoolProp as CP

import pandas as pd
import numpy as np 
import seaborn as sns
sns.set_style("darkgrid")
import math as mt
import matplotlib.pyplot as plt
import warnings
# warnings.filterwarnings("ignore")

import time
from datetime import datetime

import os
import os.path


### Constants
# Define the refrigerant (Working Fluid)
refrigerant = 'R410A'

def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files in temporary folder deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


def get_valid_input(prompt, input_type):
    while True:
        try:
            user_input = input(prompt)
            if input_type in ['day', 'month']:
                value = int(user_input)
                if input_type == 'day' and 1 <= value <= 31:
                    return f"{value:02}"  # Ensure two digits (e.g., '01', '10')
                elif input_type == 'month' and 1 <= value <= 12:
                    return f"{value:02}"  # Ensure two digits (e.g., '01', '12')
                else:
                    raise ValueError(f"{input_type.capitalize()} must be within the correct range.")
            elif input_type == 'year':
                value = int(user_input)
                if value < 100:  # Convert to two-digit format if necessary
                    return f"{value:02}"
                elif value > 2000: # To handle four-digit format if necessary
                    value = value - 2000
                    return f"{value:02}"
            elif input_type == 'hour':
                value = int(user_input)
                if 0 <= value <= 23:
                    return f"{value:02}"
                else:
                    raise ValueError("Hour must be between 0 and 23.")
            elif input_type == 'minute':
                value = int(user_input)
                if 0 <= value <= 59:
                    return f"{value:02}"
                else:
                    raise ValueError("Minute must be between 0 and 59.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            
            
def get_timestamp():
    day = get_valid_input("Enter the day (1-31): ", 'day')
    month = get_valid_input("Enter the month (1-12 or month name): ", 'month')
    year = get_valid_input("Enter the year (e.g., 2024): ", 'year')
    hour = get_valid_input("Enter the hour (0-23): ", 'hour')
    minute = get_valid_input("Enter the minute (0-59): ", 'minute')


    return f'{day}/{month}/{year} {hour}:{minute}'


def filter_dataframe(df):
    return df[df['Time Stamp'].dt.hour.between(9, 17)]
    # start_stamp = (pd.to_datetime(df['Time Stamp'], dayfirst=True, format="%d/%m/%y %H:%M")).min()
    # end_stamp = (pd.to_datetime(df['Time Stamp'], dayfirst=True, format="%d/%m/%y %H:%M")).max()
    # print(f'You have time range between {start_stamp} and {end_stamp}.')
    # user_input = input('Do you want to filter the data for certain operational hours?: yes/no ')
    # if user_input.lower() in ['yes', 'y']:
    #     print("Enter start timestamp:")
    #     start_timestamp = get_timestamp()
    #     print("*"*120)
    #     print("Enter end timestamp:")
    #     end_timestamp = get_timestamp()
    #     print("*"*120)

    #     # Ensure start timestamp is before end timestamp
    #     if start_timestamp >= end_timestamp:
    #         print("Start timestamp must be before end timestamp. Please try again.")
    #         print("*"*120)
    #         return filter_dataframe(df)

    #     # Filter the dataframe based on the provided timestamps
    #     filtered_df = df[(df['Time Stamp'] >= start_timestamp) & (df['Time Stamp'] <= end_timestamp)]
    #     return filtered_df
    
    # elif user_input.lower() in ['no', 'n']:
    #     print("*"*120)
    #     return df
    # else:
    #     print('Not a Valid input, Please try again.')
    #     print("*"*120)
    #     return filter_dataframe(df)
    

#We will identify each row belongs to which of the four systems

def sys_identify(unit_type, system_number, generic_system_number):
    if unit_type == "outdoors":
        return str(int(generic_system_number))
    elif unit_type == 'indoors':
        return str(int(system_number))
    else:
        print("NO systems found please check the data", unit_type)
    
    return None

def transform_system(df):
    values = df.values.reshape(1,-1)
    old_cols = df.columns.values
    new_cols = np.array([f'{col}.{i}' if i<df.shape[0] else f'{col}' for i in range(1,df.shape[0]+1) for col in old_cols])
    
    df = pd.DataFrame(data=values, columns=new_cols)
    return df

def combine_sys_unit(df):
    gp_object = df.groupby(by=['Time Stamp'])
    
    timer_start = time.time()
    print('Transforming Dataset in progress .........')

    df_final = pd.DataFrame()
    for name,gp in gp_object:
        if gp['Unit Type'].nunique() == 2: # Because at some time stamps the outdoor data doesn't exist
            gp.drop_duplicates(inplace = True) # Drop duplicated rows in each group
            df_final = pd.concat([df_final, transform_system(gp)], ignore_index=True)
            num_of_indoors = int(gp.shape[0]-1)
        else:
            pass
#         break

    timer_end = time.time()
    print(f'Transforming Dataset to one row per system took {timer_end - timer_start} secs to run')
    
    
    if df_final.size:
        return df_final,num_of_indoors
    else:
        return None, None

### Columns to drop

#- AirNet Addr., Backup ope., CA Device Line Number, Comp.1 current.1, Comp.2 current.1, Defrost, Demand stepping down cntl,
#Demand state, Disch. pipe retry, EVJ (refrigerant injection), EVJ (refrigerant injection) , EVM (Main), 
#EVT (subcooling heat xchanger), Error Code, HP, HVAC Unit type, Heat exchanger liquid pipe temp..1, I/U thermostat ON capacity,
#INV1 stand-by, INV1 oil separator below, INV2 stand-by, INV2 oil separator below, Low pressure retry, Oil return, 
#Operation output, Outdoor Type, Overheating stand-by, Restart stand-by, Startup control.1, 
#Subcooling heat exchanger liquid temp..1, System HP, System HP.1, Unit Type, Ventilation , 'Centralised Address','
#Cool/Heat parallel ope.','Cooling','Heating', 'Generic system number', 'Refrigerant System Number'

#- *Failure.(1 - 11) , *Line quality.(1-11) , *Working hours.(1-11), Air Thermistor BRC1 T°.(1-11), AirNet Addr..(1-11), 
#CA Device Line Number.(1-11), Central Address.1.(1-11), Filter status.(1-11), Indoor Type Code.(1-11), 
#Indoor therm ON status.(1-11), Suction T°.(1-11), System Identifier.(1-11), Time Stamp.(1-11),f'Central Address.(1-11)',
#f'Centralised Address.(1-11)', f'Indoor Type Code.(1-11)', f'Mode.(1-11)', f'Site temperature.(1-11)', f'System number.(1-11)'

#- Defrost.(1-6), HP.(1-6)

#- Error Code.(1-10)

#- Fan Mode.(1-4).(1-11), Mode.(1-6).(1-11),  Unit Type.(1-2).(1-11), Unit Type.(3-11)

#- Multiple columns same name: Unit Type.(1-2)


def cols_to_drop(k):
    lst = []
    
    lst.extend(['AirNet Addr.', 'Backup ope.', 'CA Device Line Number', 'Comp.1 current.1', 'Comp.2 current.1', 'Defrost', 
               'Demand stepping down cntl','Demand state', 'Disch. pipe retry', 'EVJ (refrigerant injection)', 
                'EVM (Main)', 'EVT (subcooling heat xchanger)', 'Error Code', 'HP', 'HVAC Unit type', 
               'Heat exchanger liquid pipe temp..1', 'I/U thermostat ON capacity', 'INV1 stand-by', 'INV1 oil separator below', 
               'INV2 stand-by', 'INV2 oil separator below', 'Low pressure retry', 'Oil return', 'Operation output', 'Outdoor Type',
               'Overheating stand-by', 'Restart stand-by', 'Startup control.1', 'Subcooling heat exchanger liquid temp..1', 
               'System HP', 'System HP.1', 'Unit Type', 'Ventilation', 'Centralised Address','Cool/Heat parallel ope.',
               'Cooling','Heating', 'Generic system number', 'Refrigerant System Number'])
    
    for i in range(1,k+1):
        for j in range(1,k+1):

            if i<=6:
                lst.append(f'Mode.{i}.{j}')
                if i<=2:
                    lst.append(f'Unit Type.{i}.{j}')
                if i<=4:
                    lst.append(f'Fan Mode.{i}.{j}')
                    
        lst.extend([f'*Failure.{i}' , f'*Line quality.{i}' , f'*Working hours.{i}', f'Air Thermistor BRC1 T°.{i}',
                   f'AirNet Addr..{i}', f'CA Device Line Number.{i}', f'Central Address.1.{i}',
                   f'Filter status.{i}', f'Indoor therm ON status.{i}',f'Suction T°.{i}', f'System Identifier.{i}',
                    f'Time Stamp.{i}', f'Central Address.{i}',f'Centralised Address.{i}', f'Indoor Type Code.{i}', 
                    f'Mode.{i}', f'Site temperature.{i}', f'System number.{i}'])
        
        lst.append(f'Unit Type.{i}')
        
        if i<=10:
            lst.append(f'Error Code.{i}')
        
        if i<=6:
            lst.extend([f'Defrost.{i}', f'HP.{i}'])
            
    return lst


def clean_combined_sys_df(df,k):
    print(f'Dataframe started with {df.shape[1]} columns.')
    # Will drop the columns that are completely Nulls
    df.dropna(axis=1, how='all', inplace = True)
    
    print(f'After removing Null columns we have {df.shape[1]} columns.')
    # Will create a list of columns to drop based on analysis
    lst_to_drop = cols_to_drop(k)
    df = df.drop(lst_to_drop , axis=1)
    
    print(f'Final Dataframe after dropping all unnecessary columns, we have {df.shape[1]} columns.')
    print('*'*100)
    
    return df

def get_final_dfs(lst_of_systems_dfs):
    dict_of_final_dfs = {}
    for i,sys_df in enumerate(lst_of_systems_dfs):
        df_unclean_i,k_i = combine_sys_unit(sys_df)
        if k_i:
            df_final = clean_combined_sys_df(df_unclean_i,k_i)
            dict_of_final_dfs[f'sys_{i}_df'] = df_final
        
    return dict_of_final_dfs


def data_transform_and_split(df):
    # df['System Identifier'] = list(map(sys_identify, df['Unit Type'], df['Unit Name']))
    df['System Identifier'] = list(map(sys_identify, df['Unit Type'], df['System number'],df['Generic system number']))

    ## We will divide the main dataframe dynamically, so that we have a dataframe for each system
    
    dict_of_systems = {}
    for i in range(df['System Identifier'].nunique()):
#         print(i)
        dict_of_systems[f'df_{i}'] = df[df['System Identifier']== f'{i}']
        
    directory_path = './outputs/Temporary'
    delete_files_in_directory(directory_path)
    
    print('.'*100)
    
    
    # make a log file to record existing systems to be used in other scripts dynamically (V0.02)
    # Temporary record just for this run only (will be used in calculating COP and making plots)
    sys_tempo_log = df['System Identifier'].drop_duplicates().sort_values()
    sys_tempo_log.to_csv(f'./outputs/Temporary/tempo_unique_sys.csv', index=False)
    
    # Permenant record will be used in calculating uncertainity for all systems 
    # if previously we entered 3 systems and today we enter 1 system only from them 
    # it should calculate uncertainity for 3 systems
    sys_tempo_log = pd.DataFrame(sys_tempo_log)
    check_file_exist(sys_tempo_log, f'./outputs/Clean transformed data before calculation/unique_sys.csv', data_df=False)
    sys_log = pd.read_csv(f'./outputs/Clean transformed data before calculation/unique_sys.csv')
    sys_log.drop_duplicates(inplace=True)
    sys_log.sort_values(by='System Identifier', inplace=True)
    sys_log.to_csv(f'./outputs/Clean transformed data before calculation/unique_sys.csv', index=False)


    lst_of_systems_dfs = list(dict_of_systems.values())
    results_dict = get_final_dfs(lst_of_systems_dfs)
    
    for name,df in results_dict.items():
        df.sort_index(axis=1, inplace=True)
        df.to_csv(f'./outputs/Temporary/sys_{name.split("_")[1]}_df.csv', index=False)
        df = check_file_exist(df.sort_index(axis=1),f'./outputs/Clean transformed data before calculation/sys_{name.split("_")[1]}_df.csv')
    
    print("Transformed data files was saved to temporary folder successfully")
    
        
        
def check_file_exist(df, path,data_df=True):
    try:
        df_temp = pd.read_csv(path,index_col=False)
    except:
        pass
    else:
        if data_df:
            df = pd.concat([df_temp,df])
            df.drop_duplicates(subset='Time Stamp',keep='first', inplace=True, ignore_index=False)
        else:
            df = pd.concat([df_temp, df])
    finally:
        df.to_csv(path, index=False)
    
def get_csv_file():
    # Prompt the user to enter the CSV file name or file path.
    # If the file is in the same directory as this script, enter just the file name (e.g., 'raw_data.csv').
    # Example: file_name = 'raw_data.csv'
    #
    # If the file is in a different directory, provide the relative or absolute path.
    # Example of a relative path: file_name = 'data/raw_data.csv' (assuming 'data' is a subdirectory)
    # Example of a relative path: file_name = '../raw_data.csv' (assuming 'raw_data.csv' exist just in the parent directory)
    # Example of an absolute path: file_name = 'C:/Users/Username/Documents/raw_data.csv'

    file_name = input('Please enter raw data csv file name or file path (e.g., raw_data.csv): ')

    try:
        # Attempt to read the CSV file using the provided file name or path.
        df = pd.read_csv(f"./Raw Data/{file_name}", low_memory=False)
        print('File was read successfully!')
        print("*"*120)
        df = filter_dataframe(df)
        df = df.dropna(how='all')
        return df
    except FileNotFoundError:
        # If the file is not found, inform the user and prompt them to enter a valid file name or path.
        print('Please enter a valid file name or file path.')
        print('*' * 120)
        # Recursively call the function to allow the user to try again.
        get_csv_file()
        
    


# data_transform_and_split(get_csv_file())

