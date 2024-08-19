import CoolProp.CoolProp as CP
import pandas as pd
import numpy as np 
import seaborn as sns
import math as mt
import matplotlib.pyplot as plt
import warnings
from env import base_aggregation,cu_agg,fcu_agg
def COP(outfile,sample_time):
    warnings.filterwarnings("ignore")

    pd.set_option('display.max_rows', 120)

    pd.set_option('display.max_columns', 120)

    df = pd.read_csv(outfile,encoding='utf-8')
    
    df.head(2)

    # A function that takes a subset dataframe
    def subset_df(main_df, filter_col, filter_values):
        res = df[df[filter_col] == filter_values]
        print(f'The Subset dataframe have the shape: {res.shape}')
        
        # Drop the columns that is completely nulls
        res = res.dropna(axis=1, how= 'all')
        print(f'Removing the complete null columns and we then have the shape: {res.shape}')
        return res

    # Make a dataframe for indoor units only named fcu_df and based on (Unit Type) -> (indoor)
    fcu_df = subset_df(main_df = df, filter_col = 'Unit Type', filter_values ='indoors')

    # Make a column to identify the system according to Unit name (system indicate which outdoor unit it's connected with)
    fcu_df['System Identifier'] = fcu_df['Unit Name'].map(lambda x: x.split('.')[1][0])

    # See the counts for each unique value
    pd.DataFrame(fcu_df['System Identifier'].value_counts()).T

    # Seems to have a typo error that results in an additional non existing system (replace with correct value)
    # fcu_df['Unit Name'] = fcu_df['Unit Name'].replace(to_replace= 'L1.048.05D2', value= 'L1.248.05D2')

    # Repeat the process to update the system identifier column values
    fcu_df['System Identifier'] = fcu_df['Unit Name'].map(lambda x: x.split('.')[1][0])
    fcu_df['System Identifier'] = fcu_df['System Identifier'].astype('int64')

    # Make sure that only 4 systems exist
    pd.DataFrame(fcu_df['System Identifier'].value_counts()).T

    # Make a dataframe for outdoor units only named cu_df and based on (Unit Type) -> (outdoor)
    cu_df = subset_df(main_df = df, filter_col = 'Unit Type', filter_values ='outdoors')


    # Function that checks that two dataframes are compaitable based on a common column
    def ensure_compaitability(df1, df2, common_col):
        df1_nunique = df1[common_col].nunique()
        df2_nunique = df2[common_col].nunique()
        
        if df1_nunique == df2_nunique:
            print(f'The two Dataframes are compaitable based on {common_col}')
        else:
            print(f"""There are differences which indicates that:
    there are some values of {common_col} column that exists in one dataframe but not the other""")
            
            # Get the intersection of values of the common column in both dataframes
            intersection = list(set(df1[common_col]) & set(df2[common_col]))
            
            # Remove the values in the common column that are not common in both dataframes so they become compaitable
            condition_df1 = [True if val in intersection else False for val in df1[common_col]]
            df1 = df1[condition_df1]
            print(f"New df1 shape: {df1.shape}")
            
            condition_df2 = [True if val in intersection else False for val in df2[common_col]]
            df2 = df2[condition_df2]
            print(f"New df2 shape: {df2.shape}")
            
        return df1,df2


    cu_df,fcu_df = ensure_compaitability(df1= cu_df, df2= fcu_df, common_col='Time Stamp')

    cu_df,fcu_df = ensure_compaitability(df1= cu_df, df2= fcu_df, common_col='Time Stamp')

    cu_df['System Identifier'] = cu_df['Centralised Address']

    cu_df['System Identifier'] = cu_df['System Identifier'].replace([11,311,111,211],[2,4,3,1])

    cu_df.head(2)

    # Ensure 'Time Stamp' is in datetime format for fcu_df
    fcu_df['Time Stamp'] = pd.to_datetime(fcu_df['Time Stamp'])
    unique_identifiers = fcu_df['System Identifier'].unique()

    resampled_dfs = []

    for identifier in unique_identifiers:
        df_identifier = fcu_df[fcu_df['System Identifier'] == identifier].copy()
        
        df_identifier.set_index('Time Stamp', inplace=True)
    
        df_identifier = df_identifier[~df_identifier.index.duplicated(keep='first')]
        df_resampled = df_identifier.resample(sample_time).agg(fcu_agg)
        df_resampled.ffill(inplace=True)
        df_resampled.reset_index(inplace=True)
        resampled_dfs.append(df_resampled)
    fcu_df_resampled = pd.concat(resampled_dfs, ignore_index=True)
    
    fcu_df = fcu_df_resampled

    # Ensure 'Time Stamp' is in datetime format for cu_df
    cu_df['Time Stamp'] = pd.to_datetime(cu_df['Time Stamp'])
    unique_identifiers_cu = cu_df['System Identifier'].unique()

    resampled_dfs_cu = []

    for identifier in unique_identifiers_cu:
        df_identifier = cu_df[cu_df['System Identifier'] == identifier].copy()
        
        df_identifier.set_index('Time Stamp', inplace=True)
        # Remove duplicate timestamps
        df_identifier = df_identifier[~df_identifier.index.duplicated(keep='first')]

        # Resample and aggregate only the existing columns
        df_resampled = df_identifier.resample(sample_time).agg(cu_agg)
        df_resampled = df_resampled.reindex(df_identifier.index)

        # Fill missing data forward (or use a different method if preferred)
        df_resampled.ffill(inplace=True)
        
        # Reset index to make 'Time Stamp' a column again
        df_resampled.reset_index(inplace=True)
        
        resampled_dfs_cu.append(df_resampled)

    # Concatenate all resampled DataFrames into a single DataFrame
    cu_df_resampled = pd.concat(resampled_dfs_cu, ignore_index=True)
    cu_df = cu_df_resampled


    fcu_df = fcu_df.set_index('Time Stamp')
    to_drop_cols_fcu = fcu_df.select_dtypes('object').columns.to_list()

    fcu_df.drop(to_drop_cols_fcu, inplace=True, axis=1)
    fcu_agg.pop('System Identifier')

    fcu_gp = fcu_df.groupby(by=['Time Stamp', 'System Identifier']).agg(fcu_agg).reset_index()



    cu_df = cu_df.set_index('Time Stamp')

    to_drop_cols_cu = cu_df.select_dtypes('object').columns.to_list()


    cu_df.drop(to_drop_cols_cu, inplace=True, axis=1)
    cu_agg.pop('System Identifier')
    cu_gp = cu_df.groupby(by=['Time Stamp', 'System Identifier']).agg(cu_agg).reset_index()

    # Ensure DataFrames have the same index for comparison

    cu_gp = cu_gp.reset_index()
    fcu_gp = fcu_gp.sort_values(by=['Time Stamp', 'System Identifier']).reset_index(drop=True)
    cu_gp = cu_gp.sort_values(by=['Time Stamp', 'System Identifier']).reset_index(drop=True)

    # Print index alignment to debug
    print("fcu_gp index:", fcu_gp.index)
    print("cu_gp index:", cu_gp.index)

    # Make sure that the data coincides so each row corresponding to the row at the same index in the other dataframe
    
    print((fcu_gp['Time Stamp'] == cu_gp['Time Stamp']).all())
    print((fcu_gp['System Identifier'] == cu_gp['System Identifier']).all())



    # Define the refrigerant (Working Fluid)
    refrigerant = 'R410A'

    # def calc_enthalpy(temperature_k, pressure_pa, refrigerant):
    #     # Ensure temperature and pressure are pandas Series
    #     assert isinstance(temperature_k, pd.Series), "temperature_k must be a pandas Series"
    #     assert isinstance(pressure_pa, pd.Series), "pressure_pa must be a pandas Series"
    #     temperature_k, pressure_pa = temperature_k.align(pressure_pa, join='inner')
    #     assert len(temperature_k) == len(pressure_pa), "temperature_k and pressure_pa must have the same length"

    #     # Calculate enthalpy using CoolProp for each row
    #     enthalpy = temperature_k.apply(lambda T: CP.PropsSI('H', 'T', T, 'P', pressure_pa.iloc[temperature_k.tolist().index(T)], refrigerant))
        
    #     return enthalpy

    def calc_enthalpy(temperature_k, pressure_pa, refrigerant):
        # Ensure temperature and pressure are pandas Series
        assert isinstance(temperature_k, pd.Series), "temperature_k must be a pandas Series"
        assert isinstance(pressure_pa, pd.Series), "pressure_pa must be a pandas Series"
        
        # Align temperature and pressure Series
        temperature_k, pressure_pa = temperature_k.align(pressure_pa, join='inner')
        assert len(temperature_k) == len(pressure_pa), "temperature_k and pressure_pa must have the same length"

        # Remove NaN values
        valid_data = temperature_k.notna() & pressure_pa.notna()
        temperature_k = temperature_k[valid_data]
        pressure_pa = pressure_pa[valid_data]
        
        # Round temperature values for comparison
        temperature_k_rounded = temperature_k.round()

        # Create a mapping from rounded temperature to pressure values
        temp_to_pressure = pressure_pa.groupby(temperature_k_rounded).first()

        def compute_enthalpy(T):
            rounded_T = round(T)
            if rounded_T in temp_to_pressure.index:
                pressure = temp_to_pressure[rounded_T]
                return CP.PropsSI('H', 'T', T, 'P', pressure, refrigerant)
            else:
                print(f"Temperature {T} not found in pressure series")
                return float('nan')

        # Apply the function to the rounded temperatures
        enthalpy = temperature_k.apply(compute_enthalpy)

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
        entropy = P_in_pa.apply(lambda P: CP.PropsSI('S', 'P', P, 'T', T_in_k.iloc[P_in_pa.tolist().index(P)], refrigerant))
        isen_enthalpy = entropy.apply(lambda S:CP.PropsSI('H', 'S', S, 'P', P_out_pa.iloc[entropy.tolist().index(S)], refrigerant))   # Enthalpy in (J/kg )                         
                                
        return isen_enthalpy

    def calc_isen_efficiency(h_isen_j_kg, h_act_out_j_kg , h_suc_j_kg):
        eta_isen = (h_isen_j_kg - h_suc_j_kg ) / (h_act_out_j_kg - h_suc_j_kg)
        
        return eta_isen

    def calc_enthalpy_dis_act(P_in_pa, T_in_k,P_out_pa, refrigerant, h_suc_j_kg):
        eta_isentropic = 0.75
        h_isen_j_kg = calc_isen_enthalpy(P_in_pa, T_in_k, P_out_pa, refrigerant)
        
        h_comp_dis_j_kg = ((h_isen_j_kg - h_suc_j_kg ) / eta_isentropic) + h_suc_j_kg
        
        return h_comp_dis_j_kg

    res = pd.DataFrame()

    res['Time Stamp'] = cu_gp['Time Stamp']
    res['T_comp1_dis (K)'] = cu_gp["INV1 comp. body temp"]+273 +5 # +273 to Kelvin , +5 assumption that the body is 5°c lower th
    res['T_comp2_dis (K)'] = cu_gp["INV2 comp. body temp"]+273 +5
    res['P_cond (Pa)'] = cu_gp["Condensing Pressure"] * 1e6
    res['P_evap (Pa)'] = cu_gp["Evaporating Pressure"] * 1e6
    res['T_comp_suc (K)'] = cu_gp["Comp. suction pipe temp."]+273

    # Adding target efficiency columns
    res['target_eta'] = [0.75]*res.shape[0]
    res['target_eta2'] = [0]*res.shape[0]

    # Calculating enthalpy values
    res['h_comp_suc (j/kg)'] = calc_enthalpy(res['T_comp_suc (K)'], res['P_evap (Pa)'], refrigerant)
    res['h_comp1_dis (j/kg)'] = calc_enthalpy(res['T_comp1_dis (K)'], res['P_cond (Pa)'], refrigerant)
    res['h_comp2_dis (j/kg)'] = calc_enthalpy(res['T_comp2_dis (K)'], res['P_cond (Pa)'], refrigerant)

    # Calculating isentropic enthalpy
    res['h_isen (j/kg)'] = calc_isen_enthalpy(res['P_evap (Pa)'], res['T_comp_suc (K)'], res['P_cond (Pa)'], refrigerant)

    # Calculating isentropic efficiencies
    res['eta_isentropic_1'] = calc_isen_efficiency(res['h_isen (j/kg)'], res['h_comp1_dis (j/kg)'], res['h_comp_suc (j/kg)'])
    res['eta_isentropic_2'] = calc_isen_efficiency(res['h_isen (j/kg)'], res['h_comp2_dis (j/kg)'], res['h_comp_suc (j/kg)'])

    # Determining conditions for isentropic efficiency that it is assumed to be within the rannge [0% to 75%]
    eta1_condition = ((res['eta_isentropic_1'] > res['target_eta']) | (res['eta_isentropic_1'] < res['target_eta2'])) | (res['h_comp1_dis (j/kg)'] <= res['h_comp_suc (j/kg)'])
    eta2_condition = ((res['eta_isentropic_2'] > res['target_eta']) | (res['eta_isentropic_2'] < res['target_eta2'])) | (res['h_comp2_dis (j/kg)'] <= res['h_comp_suc (j/kg)'])

    # Adding conditions to DataFrame
    res['eta1_condition'] = eta1_condition
    res['eta2_condition'] = eta2_condition

    # Calclating enthalpy based on 75% isentropic efficiency to replace fault values
    enthalpy_discharge_actual = calc_enthalpy_dis_act(res['P_evap (Pa)'],
                                                            res['T_comp_suc (K)'],
                                                            res['P_cond (Pa)'],
                                                            refrigerant, res['h_comp_suc (j/kg)'])

    # Updating enthalpy values based on conditions, if the isentropic efficieny falls outside the assumed range, 
    # we put the assumed isentropic efficiency (75%) and then work backwards to calculate the enthalpy to be used. 
    res.loc[eta1_condition, 'h_comp1_dis (j/kg)'] = enthalpy_discharge_actual[eta1_condition]
    res.loc[eta2_condition, 'h_comp2_dis (j/kg)'] = enthalpy_discharge_actual[eta2_condition]

    eta_e = 0.98
    voltage = 415                                                                                    # volt
    P_F = 0.8

    # Calculating electric power for each compressor
    res['comp1_mech_power'] = cu_gp["Comp.1 current"] * voltage * P_F * mt.sqrt(3) * eta_e       # watt
    res['comp2_mech_power'] = cu_gp["Comp.2 current"] * voltage * P_F * mt.sqrt(3) * eta_e       # watt



    def calc_mass_flow(comp1_mech_power, h_comp1_dis, h_comp1_suc, comp2_mech_power, h_comp2_dis):
        # Ensure all parameters are pandas Series
        assert isinstance(comp1_mech_power, pd.Series), "comp1_mech_power must be a pandas Series"
        assert isinstance(h_comp1_dis, pd.Series), "h_comp1_dis must be a pandas Series"
        assert isinstance(h_comp1_suc, pd.Series), "h_comp1_suc must be a pandas Series"
        assert isinstance(comp2_mech_power, pd.Series), "comp2_mech_power must be a pandas Series"
        assert isinstance(h_comp2_dis, pd.Series), "h_comp2_dis must be a pandas Series"
        
        # Calculate mass flow rates using vectorized operations
        m_comp1 = comp1_mech_power / (h_comp1_dis - h_comp1_suc)
        
        m_comp2 = comp2_mech_power / (h_comp2_dis - h_comp1_suc)
        
        m_total = m_comp1 + m_comp2
        
        return m_comp1.tolist(), m_comp2.tolist(), m_total.tolist()


    res['m_comp1'], res['m_comp2'], res['m_total'] = calc_mass_flow( comp1_mech_power = res['comp1_mech_power'],
                                                                h_comp1_dis = res['h_comp1_dis (j/kg)'],
                                                                h_comp1_suc = res['h_comp_suc (j/kg)'],
                                                                comp2_mech_power = res['comp2_mech_power'],
                                                                h_comp2_dis = res['h_comp2_dis (j/kg)'])

    res['T_evap_ex (K)'] = fcu_gp['Gas Pipe T°'] + 273
    res['T_subcooling (K)'] = cu_gp['Subcooling heat exchanger liquid temp.'] + 273

    res['h_evap_ex (j/kg)'] = calc_enthalpy(res['T_evap_ex (K)'],res['P_evap (Pa)'],refrigerant)
    res['h_evap_in (j/kg)'] = calc_enthalpy(res['T_subcooling (K)'],res['P_cond (Pa)'],refrigerant)

    res['cooling_load (KW)'] = res['m_total'] * (res['h_evap_ex (j/kg)'] - res['h_evap_in (j/kg)']) / 1000

    res['Total_electric_power (KW)'] = cu_gp['*Electric Power (Estimated)'] + res['comp1_mech_power'] / (1000*0.98) + res['comp2_mech_power'] / (1000*0.98)

    res['COP'] = res['cooling_load (KW)'] / (res['Total_electric_power (KW)'])
    res['COP'] = res['COP'].fillna(0)

    res['COP'].isnull().sum()

    res.to_csv('res.csv', index=False)

    fcu_gp.to_csv('fcu.csv', index=False)

    cu_gp.to_csv('cu.csv', index=False)

    res = res.set_index('Time Stamp')
    res.head(3)

    fcu_gp.rename(columns={'System Identifier':'System Identifier fcu'}, inplace=True)
    fcu_gp = fcu_gp.set_index('Time Stamp')
    fcu_gp.head(3)

    cu_gp.rename(columns={'System Identifier':'System Identifier cu'}, inplace=True)
    cu_gp = cu_gp.set_index('Time Stamp')
    cu_gp.head(3)

    final_result = pd.concat([fcu_gp, cu_gp, res], axis=1)
    final_result = final_result.reset_index()
    final_result

    # Drop columns that are repeated and not necessary
    cols_drop = ['AirNet Addr.','Centralised Address','CA Device Line Number','*Line quality','Site temperature']
    df.drop(df[cols_drop], axis=1, inplace=True)

    final_result.to_csv('Final_results.csv', index=False)

    sns.set_style("darkgrid")


    df1 = pd.read_csv('Final_results.csv')
    (df1['System Identifier cu'] == df1['System Identifier fcu']).sum()
    # Completely identical (make one column and remove other)
    df1['System Identifier'] = df1['System Identifier cu']
    df1.drop(['System Identifier cu','System Identifier fcu'], axis=1, inplace=True)
    df1.head(2)

    columns_keep = [
        'Time Stamp', 'm_total', 'h_evap_ex (j/kg)', 'h_evap_in (j/kg)',
        'cooling_load (KW)', 'Total_electric_power (KW)', 'COP', 'System Identifier'
    ]

    df = df1[columns_keep]

    df.rename(columns={'h_evap_ex (j/kg)':'(c) Evaporator outlet enthalpy (kj/kg)',
                    'h_evap_in (j/kg)':'(d) Evaporator inlet enthalpy (kj/kg)',
                    'm_total' : '(b) Mass Flow Rate (kg/sec)',
                    'Total_electric_power (KW)': '(a) Total electric power (KW)',
                    'cooling_load (KW)': '(g) Cooling Load (Heat Gain) (KW)'}, inplace=True)

    df['(b) Mass Flow Rate (kg/sec)'] = df['(b) Mass Flow Rate (kg/sec)'].apply(lambda x: round(x,5))

    df['(c) Evaporator outlet enthalpy (kj/kg)'] = df['(c) Evaporator outlet enthalpy (kj/kg)']/1000
    df['(d) Evaporator inlet enthalpy (kj/kg)'] = df['(d) Evaporator inlet enthalpy (kj/kg)']/1000

    df['(f) Condenser outlet enthalpy (kj/kg)'] = df1['h_evap_in (j/kg)'] / 1000
    df['(e) Condenser inlet enthalpy (kj/kg)'] = df1['h_comp1_dis (j/kg)'] / 1000

    df.head(2)

    df['(h) Condenser Heat Reject (KW)'] = df['(b) Mass Flow Rate (kg/sec)'] * ((df['(e) Condenser inlet enthalpy (kj/kg)']) - (df['(f) Condenser outlet enthalpy (kj/kg)']))

    # Remove values of 0 Heat reject so that the result doesn't go to infinity
    df = df[df['(h) Condenser Heat Reject (KW)'] != 0]

    sorted_columns = list(df.columns.values)

    sorted_columns.sort()

    df = df[sorted_columns]


    df['(j) Percent Energy Balance (%)'] = 100 *((df['(a) Total electric power (KW)'] 
                                                + df['(g) Cooling Load (Heat Gain) (KW)']
                                                - df['(h) Condenser Heat Reject (KW)']) / (df['(h) Condenser Heat Reject (KW)']))


    df.tail(n=10)

    df.sample(n=10)

    total_data_count = df.shape[0]
    data_count_more_10_percent = df[df["(j) Percent Energy Balance (%)"] > 10].shape[0]
    data_count_less_10_percent = df[df["(j) Percent Energy Balance (%)"] < -10].shape[0]
    percent_within_10_percent = round(((total_data_count 
                                - data_count_more_10_percent 
                                - data_count_less_10_percent) / total_data_count)*100,2)
    return total_data_count,data_count_more_10_percent,data_count_less_10_percent,percent_within_10_percent

    
