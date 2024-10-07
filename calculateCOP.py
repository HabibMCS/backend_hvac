#!/usr/bin/env python
# coding: utf-8

# In[65]:


#!/usr/bin/env python
# coding: utf-8

# In[29]:


### Importing Necessary libraries

import CoolProp.CoolProp as CP

import pandas as pd
import numpy as np 
import seaborn as sns
sns.set_style("darkgrid")
import math as mt
# import matplotlib.pyplot as plt
import warnings
# warnings.filterwarnings("ignore")

import time
from datetime import datetime

import os

### Constants
# Define the refrigerant (Working Fluid)
refrigerant = 'R410A'

def read_transformed_df():
    # Get the systems dataframes dynamically
    sys_df_dict = {}
    temp_sys_log = pd.read_csv(f'.\outputs\Temporary\\tempo_unique_sys.csv')
        
    for i in temp_sys_log['System Identifier']:
        sys_df_dict[f'sys_{i}_df'] = pd.read_csv(f'.\outputs\Temporary\\sys_{i}_df.csv')
        sys_df_dict[f'sys_{i}_df'] = sys_df_dict[f'sys_{i}_df'].drop_duplicates()
        # Filter the values where difference in compressor suction temp. and evaporation temp is low for better accuracy
        sys_df_dict[f'sys_{i}_df'] = sys_df_dict[f'sys_{i}_df'][(sys_df_dict[f'sys_{i}_df']['Comp. suction pipe temp.'] 
                                                                 - sys_df_dict[f'sys_{i}_df']['Evaporating Temperature'])> 2]
        
        sys_df_list = list(sys_df_dict.values())

    return sys_df_list

### Functions to calculate properties
def calc_enthalpy(temperature_k, pressure_pa, refrigerant, phase):
    # Ensure temperature and pressure are pandas Series
    assert isinstance(temperature_k, pd.Series), "temperature_k must be a pandas Series"
    assert isinstance(pressure_pa, pd.Series), "pressure_pa must be a pandas Series"
    temperature_k, pressure_pa = temperature_k.align(pressure_pa, join='inner')
    assert len(temperature_k) == len(pressure_pa), "temperature_k and pressure_pa must have the same length"

    # Calculate enthalpy using CoolProp for each row
    try:       
        enthalpy = temperature_k.apply(lambda T: CP.PropsSI('H', 'T', T,
                                                            'P', pressure_pa.iloc[temperature_k.tolist().index(T)],
                                                            refrigerant))
    except ValueError:
        if phase == 'superheated':
            enthalpy = calc_enthalpy(temperature_k+0.1, pressure_pa, refrigerant, phase)
        elif phase == 'subcooled':
            enthalpy = calc_enthalpy(temperature_k-0.1, pressure_pa, refrigerant, phase)

    return enthalpy


def calc_isen_enthalpy(P_in_pa, T_in_k, P_out_pa, refrigerant):
    # Ensure temperature and pressure are pandas Series
    assert isinstance(T_in_k, pd.Series), "T_in_k must be a pandas Series"
    assert isinstance(P_in_pa, pd.Series), "P_in_pa must be a pandas Series"
    assert isinstance(P_out_pa, pd.Series), "P_out_pa must be a pandas Series"
    T_in_k, P_in_pa = T_in_k.align(P_in_pa, join='inner')
    T_in_k, P_out_pa = T_in_k.align(P_out_pa, join='inner')
    assert len(T_in_k) == len(P_in_pa) == len(P_out_pa), "temperature_k and pressure_pa must have the same length"
    
    # Calculate entropy using CoolProp for each row
    entropy = []
    for i,P in enumerate(P_in_pa):
        try:
            entropy.append(CP.PropsSI('S', 'P', P, 'T', T_in_k.iloc[i], refrigerant))
        except ValueError:
            entropy.append(CP.PropsSI('S', 'Q', 1,'P', P, refrigerant))

    entropy = pd.Series(entropy)
    isen_enthalpy = entropy.apply(lambda S:CP.PropsSI('H', 'S', S,
                                                      'P', P_out_pa.iloc[entropy.tolist().index(S)],
                                                      refrigerant))   # Enthalpy in (J/kg )
    
    return isen_enthalpy
    
    

def calc_isen_efficiency(h_isen_j_kg, h_act_out_j_kg , h_suc_j_kg):
    eta_isen = (h_isen_j_kg - h_suc_j_kg ) / (h_act_out_j_kg - h_suc_j_kg)
    
    return eta_isen


def calc_mass_flow(comp1_mech_power, h_comp1_dis, h_comp_suc, comp2_mech_power, h_comp2_dis):
    # Ensure all parameters are pandas Series
    assert isinstance(comp1_mech_power, pd.Series), "comp1_mech_power must be a pandas Series"
    assert isinstance(h_comp1_dis, pd.Series), "h_comp1_dis must be a pandas Series"
    assert isinstance(h_comp_suc, pd.Series), "h_comp1_suc must be a pandas Series"
    assert isinstance(comp2_mech_power, pd.Series), "comp2_mech_power must be a pandas Series"
    assert isinstance(h_comp2_dis, pd.Series), "h_comp2_dis must be a pandas Series"
    
    # Calculate mass flow rates using vectorized operations
    m_comp1 = comp1_mech_power / (h_comp1_dis - h_comp_suc)
    m_comp2 = comp2_mech_power / (h_comp2_dis - h_comp_suc)
    m_total = m_comp1 + m_comp2
    return m_comp1.tolist(), m_comp2.tolist(), m_total.tolist()


def correct_comp2_delta_t(x):
        if x >=10:
            y = 12
        elif x>=8: 
            y = 9
        elif x>=6:
            y= 7
        elif x>=5:
            y= 5
        elif x>=4:
            y = 3
        elif x>3:
            y = 1
        elif x>=1:
            y=-2
        elif x>=0:
            y = 0

        return y
    
def remove_unecessary_files():
    temp_sys = pd.read_csv(f'.\outputs\Temporary\\tempo_unique_sys.csv')
    tot_sys = pd.read_csv(f'.\outputs\Clean transformed data before calculation\\unique_sys.csv')

    intersection = set(temp_sys['System Identifier']) & set(tot_sys['System Identifier'])

    missing_sys = tot_sys.drop(index=intersection)

    for i in missing_sys['System Identifier']:
        if os.path.exists(f'.\outputs\Results with outliers\\results.{i}.csv'):
              os.remove(f'.\outputs\Results with outliers\\results.{i}.csv')
    
def remover_outliers(sys_df):
    for col in ['COP','cooling_load (KW)']:
        Q1 = sys_df[col].quantile(0.25)
        Q3 = sys_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR

        lower_outliers = sys_df[sys_df[col] < lower_fence][col].sys_dfs
        upper_outliers = sys_df[sys_df[col] > upper_fence][col].sys_dfs

        sys_df[col].replace(lower_outliers, lower_fence, inplace=True)
        sys_df[col].replace(upper_outliers, upper_fence, inplace=True)
    return sys_df

def perform_calculations(sys_df,z):
    print(f'Performing Calculations for system {z} in Progress .....')

    
    ### Calculating the mass fractions for each evaporator
    sys_df['EV total'] = sys_df.loc[:,'EV Opening.1':'EV Opening.9'].sum(axis=1)
    counter = sys_df.loc[:,'EV Opening.1':'EV Opening.9'].shape[1]
    for i in range(1,counter+1):
        sys_df[f'mass_fraction.{i}'] = sys_df[f'EV Opening.{i}'] / (sys_df['EV total']+0.000001)  
        # adding 0.000001 enures the we don't divide by zero


    # sys_df

    #Now we will calculate the enthalpies at each evaporator inlet and exit

    # Note that all pressures are considered guage pressures and should be converted to absolute pressures as follows:
    # P_absolute = P_guage + P_atm    

    P_atm = 101325 #pa

    # Note that we will use 'mt.ceil' and 'mt.floor' functions to avoid the error of two phase flow input and to avoid calculating 
    # enthalpy for superheated vapor when it's supposed to be subcooled fluid and vice-versa

    counter = sys_df.loc[:,'EV Opening.1':'EV Opening.9'].shape[1]
    for i in range(1,counter+1):
        #identify evaporator exit temperature in (K) for each evaportator
        sys_df[f'T_evap_ex.{i}'] = sys_df[f'Gas Pipe T°.{i}'].apply(lambda x: mt.ceil(x+273.15))
        #Calculate enthalpy at each evaporator exit in (j/kg) using evaporating pressure in (pa)
        sys_df[f'h_evap_ex.{i}'] = calc_enthalpy((sys_df[f'T_evap_ex.{i}']),((sys_df['Evaporating Pressure']* 1e6)+P_atm)
                                                   ,refrigerant,phase='superheated')




    # for evaporator inlet, we will first get the temp. of condenser exit, and then calculate the enthalpy which will be the same
    #enthalpy for each evaporator inlet after the refrigerant passes through each expansion valve (constant enthalpy process)    
    sys_df['T_cond_ex'] = sys_df['Subcooling heat exchanger liquid temp.'].apply(lambda x: mt.floor(x+273.15))
    sys_df['h_evap_in'] = calc_enthalpy((sys_df['T_cond_ex']),
                                        ((sys_df['Condensing Pressure']* 1e6)+P_atm),
                                        refrigerant,phase='subcooled')



    # Now we calculate delta-enthalpy for each evaporator and multiply each by its corresponding mass fraction and then adding them
    # together to have the 'Total Cooling effect' of the system which when multiplied by total mass flow rate will give
    # the 'Total Cooling Load' of that system

    counter = sys_df.loc[:,'EV Opening.1':'EV Opening.9'].shape[1]
    for i in range(1,counter+1):
        # delta-enthalpy for each evaporator and multiply each by its corresponding mass fraction  in (j/kg)
        sys_df[f'cooling_effect.{i}'] = (sys_df[f'h_evap_ex.{i}'] - sys_df['h_evap_in']) * (sys_df[f'mass_fraction.{i}'])



    sys_df.sort_index(axis=1,inplace=True)
    sys_df['cooling_effect_total'] = sys_df.loc[:,'cooling_effect.1':'cooling_effect.9'].sum(axis=1)  # in (j/kg)


    ### Calculate required properties

    #h_discharge & h_suction for compressor 1 and compressor 2

    # We have the issue that the column 'Discharge pipe temp.(Comp.2)' is misleading as it contains unrealistic temperatures
    # based on operating conditions, and also the compressor body temperature 'INV2 comp. body temp' is not accurate to use as well
    # because the margin between Discharge pipe temp. and comp. body temp. is not constant but it depends on whether the comp.
    # is operating or not, so we can take the margin of comp.1 as a guidance to estimate the value of discharge pipe temp. of comp.2


    # Make columns to indicate when comp.1 is operating and also for comp.2  (1-> comp. running, 0-> comp. is not running)
    sys_df['Comp1_operating'] = sys_df['Comp.1 current']>0
    sys_df['Comp1_operating'] = sys_df['Comp1_operating'].apply(lambda x: int(x))

    sys_df['Comp2_operating'] = sys_df['Comp.2 current']>0
    sys_df['Comp2_operating'] = sys_df['Comp2_operating'].apply(lambda x: int(x))

    # let' understand the relation between discharge temp. and comp. body temp. for comp.1
    # sns.histplot(data=sys_df, x=(sys_df['Discharge pipe temp.(Comp.1)'] - sys_df['INV1 comp. body temp'])
    #              ,hue='Comp1_operating', bins=5)
    # plt.show()

    # we can see that when the compressor is not running discharge temp. is equal or less than body temp.
    # and when the compressor is running the discharge temp. is higher than body temp. by 5, 10, or 15°C

    # let's see the relation of that difference with compressor current
    # sns.lineplot(data=sys_df, x='Comp.1 current'
    #              , y=(sys_df['Discharge pipe temp.(Comp.1)'] - sys_df['INV1 comp. body temp']))
    # plt.ylabel('Discharge temp. - Body temp.')
    # plt.yticks(np.linspace(-4,16,11))
    # plt.xticks(np.linspace(0,12,13))
    # plt.grid()
    # plt.show()

    # To mimic this behaviour for compressor 2 we can say:
    # If compressor 2 current is between (0 and 1) then discharge temp. = body temp.
    # If compressor 2 current is between (1 and 3) then discharge temp. = body temp. - 2°C
    # If compressor 2 current is between (3 and 4) then discharge temp. = body temp. + 1°C
    # If compressor 2 current is between (4 and 5) then discharge temp. = body temp. + 3°C
    # If compressor 2 current is between (5 and 6) then discharge temp. = body temp. + 5°C
    # If compressor 2 current is between (6 and 8) then discharge temp. = body temp. + 6.5°C
    # If compressor 2 current is between (8 and 10) then discharge temp. = body temp. + 9°C
    # If compressor 2 current is larger than (10) then discharge temp. = body temp. + 12°C
    
    sys_df['T_comp2_dis']=(sys_df['Comp.2 current'].apply(lambda x: correct_comp2_delta_t(x))) +sys_df['INV2 comp. body temp']

    # let's now see if our function has approximated the relation close enough
    # sns.lineplot(data=sys_df, x='Comp.1 current'
    #              , y=(sys_df['Discharge pipe temp.(Comp.1)'] - sys_df['INV1 comp. body temp']))

    # sns.lineplot(data=sys_df, x='Comp.2 current'
    #              , y=(sys_df['T_comp2_dis'] - sys_df['INV2 comp. body temp']))
    # plt.ylabel('Discharge temp. - Body temp.')
    # plt.xlabel('Compressor current')
    # plt.yticks(np.linspace(-4,16,11))
    # plt.xticks(np.linspace(0,12,13))
    # plt.grid()
    # plt.show()

    # The relation seems to be good so now we can use 'T_comp2_dis' column

    # Get Compressor Discharge temp. in (K)
    sys_df['T_comp1_dis'] = sys_df['Discharge pipe temp.(Comp.1)'] + 273.15  #in (K)
    sys_df['T_comp2_dis'] = sys_df['T_comp2_dis'] + 273.15  #in (K)

    # Get Compressor Suction temp. in (K)
    sys_df['T_comp_suc'] = sys_df["Comp. suction pipe temp."]+273.15   #in (K)

    # Calculate suction and discharege enthalpies for both compressors
    sys_df['h_comp_suc'] = calc_enthalpy(sys_df['T_comp_suc'],
                                         ((sys_df['Evaporating Pressure']* 1e6)+P_atm),
                                         refrigerant,phase='superheated')     #in (j/kg)

    sys_df['h_comp1_dis'] = calc_enthalpy(sys_df['T_comp1_dis'],
                                          ((sys_df['Condensing Pressure']* 1e6)+P_atm),
                                          refrigerant,phase='superheated')     #in (j/kg)

    sys_df['h_comp2_dis'] = calc_enthalpy(sys_df['T_comp2_dis'],
                                          ((sys_df['Condensing Pressure']* 1e6)+P_atm),
                                          refrigerant,phase='superheated')     #in (j/kg)

    # We will set two limits for isentropic efficiency to prevent outlier values - 0% ~ 75%
    sys_df['target1_eta'] = [0.75]*sys_df.shape[0]
    sys_df['target2_eta'] = [0]*sys_df.shape[0]

    sys_df['h_isen (j/kg)'] = calc_isen_enthalpy(((sys_df['Evaporating Pressure']* 1e6)+P_atm), sys_df['T_comp_suc'], ((sys_df['Condensing Pressure']* 1e6)+P_atm), refrigerant)

    sys_df['eta_isentropic_1'] = calc_isen_efficiency(sys_df['h_isen (j/kg)'], sys_df['h_comp1_dis'] , sys_df['h_comp_suc'])
    sys_df['eta_isentropic_2'] = calc_isen_efficiency(sys_df['h_isen (j/kg)'], sys_df['h_comp2_dis'] , sys_df['h_comp_suc'])

    eta1_condition = ((sys_df['eta_isentropic_1'] > sys_df['target1_eta']) | (sys_df['eta_isentropic_1'] < sys_df['target2_eta'])) | (sys_df['h_comp1_dis'] <= sys_df['h_comp_suc'])
    eta2_condition = ((sys_df['eta_isentropic_2'] > sys_df['target1_eta']) | (sys_df['eta_isentropic_2'] < sys_df['target2_eta'])) | (sys_df['h_comp2_dis'] <= sys_df['h_comp_suc'])

    sys_df['eta1_condition'] = eta1_condition
    sys_df['eta2_condition'] = eta2_condition

    sys_df.loc[eta1_condition, 'h_comp1_dis'] = sys_df['h_isen (j/kg)'][eta1_condition]
    sys_df.loc[eta2_condition, 'h_comp2_dis'] = sys_df['h_isen (j/kg)'][eta2_condition]

    # sys_df

    ## Calculating Mass flow rate of comp1 and comp2

    #Assuming:
    #- Volt = 415 v  #
    #- Power Factor = 0.8  #
    #- Three phase electric motor  #
    #- Electric efficiency = 98%  #


    eta_e = 0.98
    voltage = 415                                                                                    # volt
    P_F = 0.8

    # Calculating electric power for each compressor
    sys_df['comp1_mech_power'] = sys_df["Comp.1 current"] * voltage * P_F * mt.sqrt(3) * eta_e       # watt
    sys_df['comp2_mech_power'] = sys_df["Comp.2 current"] * voltage * P_F * mt.sqrt(3) * eta_e       # watt



    # Calculating Mass flow rate at each compressor and the total mass flow rate
    sys_df['m_comp1'], sys_df['m_comp2'], sys_df['m_total'] = calc_mass_flow( comp1_mech_power = sys_df['comp1_mech_power'],
                                                                   h_comp1_dis = sys_df['h_comp1_dis'],
                                                                   h_comp_suc = sys_df['h_comp_suc'],
                                                                   comp2_mech_power = sys_df['comp2_mech_power'],
                                                                   h_comp2_dis = sys_df['h_comp2_dis'])

    # Calculating Cooling Load of the operating indoor units

    sys_df['cooling_load (KW)'] = ((sys_df['m_total'] * sys_df['cooling_effect_total']) / 1000).apply(lambda x:round(x,2))
    #in (kw)

    # Calculating Cooling Load of each operating indoor unit alone 
    for i in range(1,counter+1):
        # Modified unit cooling effect (already multiplied by mass fraction) Multiplied by Total Mass Flow Rate  in (kw)
        sys_df[f'unit_cooling_load.{i}'] = (sys_df[f'cooling_effect.{i}'] * sys_df['m_total'])/1000

    ## Calculating Total Electric Power
    
    sys_df['Total_electric_power (KW)'] = sys_df['*Electric Power (Estimated)']+ sys_df['comp1_mech_power'] / (1000*0.98) + sys_df['comp2_mech_power'] / (1000*0.98)
    # sys_df
    
    ## Calculating COP
    sys_df['COP'] = sys_df['cooling_load (KW)'] / (sys_df['Total_electric_power (KW)']+0.000000000001)
    
    sys_df.dropna(axis=0, how='any', inplace=True)
    
    # Saving the final dataframe in csv
    sys_df.to_csv(f'.\outputs\Temporary\\results.{z}.csv', index=False)
    sys_df.to_csv(f'.\outputs\Results with outliers\\results.{z}.csv', index=False)
    sys_df[:] = remover_outliers(sys_df)
    sys_df.to_csv(f'.\outputs\Results without outliers\\results.{z}.csv', index=False)  

    print(f"Calculations of system {z} performed successfully")
    print("*"*120)


# In[30]:


# Read the transformed dataframes and get them as a list
lst_of_sys_dfs = read_transformed_df()

# Perform calculations to calculate COP and Cooling Load
for z,sys_df in enumerate(lst_of_sys_dfs):
    perform_calculations(sys_df,z)
    
remove_unecessary_files()

