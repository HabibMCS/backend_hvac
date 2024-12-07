
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



def get_uncertainity_factor():
    try:
        uncertainity_factor = float(input('Please enter desired uncertainity factor (eg. 1 - 10)%: '))
    except:
        print('Invalid input, Please try again.')
        return(get_uncertainity_factor())
    return uncertainity_factor

def calculate_uncertainity_summary():
    uncertainity_factor = 10# get_uncertainity_factor()
    total_summary = pd.DataFrame()
    
    sys_log = pd.read_csv(f'./outputs/Cleantransformeddatabeforecalculation/unique_sys.csv')
    
    for i in sys_log['System Identifier']:
        new_df = pd.read_csv(f'./outputs/Resultswithoutoutliers/results.{i}.csv')

        new_df['(e) Condenser outlet enthalpy (kj/kg)'] = new_df['h_evap_in'] / 1000
        new_df['(d) Condenser inlet enthalpy (kj/kg)'] = new_df['h_comp1_dis'] / 1000

        new_df['(c) Evaporator total Cooling Effect (kj/kg)'] = new_df['cooling_effect_total'] / 1000

        columns_keep = [
            'Time Stamp', 'm_total', '(c) Evaporator total Cooling Effect (kj/kg)','cooling_load (KW)', 'Total_electric_power (KW)',
            'COP', 'System Identifier', '(e) Condenser outlet enthalpy (kj/kg)', '(d) Condenser inlet enthalpy (kj/kg)'
        ]

        new_df = new_df[columns_keep]

        new_df.rename(columns={'m_total' : '(b) Mass Flow Rate (kg/sec)',
                           'Total_electric_power (KW)': '(a) Total electric power (KW)',
                          'cooling_load (KW)': '(f) Cooling Load (Heat Gain) (KW)'}, inplace=True)

        new_df['(b) Mass Flow Rate (kg/sec)'] = new_df['(b) Mass Flow Rate (kg/sec)'].apply(lambda x: round(x,5))

        new_df['(g) Condenser Heat Reject (KW)'] = new_df['(b) Mass Flow Rate (kg/sec)'] * ((new_df['(d) Condenser inlet enthalpy (kj/kg)']) - (new_df['(e) Condenser outlet enthalpy (kj/kg)']))

        new_df.sort_index(axis=1, inplace=True)

        # Remove values of 0 Heat reject so that the result doesn't go to infinity and 0 heat reject means that the system
        # has not reached steady state conditions
        new_df = new_df[new_df['(g) Condenser Heat Reject (KW)'] != 0]

        new_df['(i) Percent Energy Balance (%)'] = 100 *((new_df['(a) Total electric power (KW)'] 
                                                    + new_df['(f) Cooling Load (Heat Gain) (KW)']
                                                    - new_df['(g) Condenser Heat Reject (KW)']) 
                                                     / (new_df['(a) Total electric power (KW)'] + new_df['(f) Cooling Load (Heat Gain) (KW)']))
        print('*'*48,f'Results Summary for system {i}','*'*49)
        if new_df.shape[0]>0:
            if new_df.shape[0]>10:
                sample_data = new_df.sample(n=10)
            else:
                sample_data = new_df

            sample_data.to_csv(f"./outputs/Uncertainitysummary/sample_sys_{i}.csv", index=False)
                
        else:
            print("This system is not operating during the filtered or specified time range")
            print("*"*120)
            if i == 3:
                print('*'*34, 'All results are saved in corresponding CSVs successfully!','*'*34)
            continue


        total_data_count = new_df.shape[0]
        more_than_uncertain_percent = new_df[new_df["(i) Percent Energy Balance (%)"] > uncertainity_factor].shape[0]
        less_than_uncertain_percent = new_df[new_df["(i) Percent Energy Balance (%)"] < - uncertainity_factor].shape[0]
        percent_data_certain = round(((total_data_count 
                                      - more_than_uncertain_percent 
                                      - less_than_uncertain_percent) / total_data_count)*100,2)
        
        summary_df = pd.DataFrame({
            f'Total Data': total_data_count,
            f'Data>{uncertainity_factor}% error': more_than_uncertain_percent,
            f'Data<-{uncertainity_factor}% error': less_than_uncertain_percent,
            f'Percent energy balance': f'{percent_data_certain} %'    
        }, index=[0])
        
        total_summary = pd.concat([total_summary,summary_df])
        
        print(summary_df)
        
        if i == 3:
            print('*'*34, 'All results are saved in corresponding CSVs successfully!','*'*34)
            
    total_summary.to_csv(f"./outputs/Uncertainitysummary/Allsystemsresultssummary.csv", index=False)
        

# calculate_uncertainity_summary()

