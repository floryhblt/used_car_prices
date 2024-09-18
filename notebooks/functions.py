import yaml
import pandas as pd
import numpy as np
import re

# dictionary to map the new values for the transmission


transmission_mapping = {
    'Automatic': ['A/T', 'Automatic', '6-Speed A/T', '8-Speed A/T', '10-Speed Automatic', 
                  'Transmission w/Dual Shift Mode', '6-Speed Automatic', '7-Speed A/T', 
                  '5-Speed Automatic', '8-Speed Automatic', '9-Speed A/T', '10-Speed A/T', 
                  '9-Speed Automatic', '5-Speed A/T', '1-Speed A/T', '4-Speed A/T',
                  '9-Speed Automatic with Auto-Shift', '8-Speed Automatic with Auto-Shift', 
                  '10-Speed Automatic with Overdrive', '1-Speed Automatic', '2-Speed Automatic', 
                  '7-Speed Automatic', '7-Speed Automatic with Auto-Shift', '6-Speed Automatic with Auto-Shift',
                  'Single-Speed Fixed Gear', '8-SPEED A/T', '7-Speed DCT Automatic', '2-Speed A/T', '4-Speed Automatic'],
    
    'Manual': ['M/T', 'Manual', '5-Speed M/T', '6-Speed M/T', '7-Speed M/T', 
               '6-Speed Manual', '7-Speed Manual', '8-Speed Manual', '6 Speed Mt', '7-Speed'],
    
    'CVT': ['Automatic CVT', 'CVT Transmission', 'Variable', 'CVT-F'],
    
    'Other': ['F', '2', '–', 'SCHEDULED FOR OR IN PRODUCTION', 'Transmission Overdrive Switch']
}





#function to import yaml file
def import_yaml():
    try:
        with open("../config.yaml", "r") as file:
            config = yaml.safe_load(file)
    except:
        print("The config.yaml file was not found in the main folder!")

    return config



# CLEANING FUNCTIONS


#function to fill Nan values of DS
def cleaning_null (df):
    
    #Cleaning 'fuel_types' that arent defined and cant find information from other columns 
    df['fuel_type'] = df['fuel_type'].replace(['–', 'not supported'], np.nan)

    # Fill missing 'fuel_type' values when the model is 'Tesla'
    df.loc[(df['fuel_type'].isnull()) & (df['brand'] == 'Tesla'), 'fuel_type'] = 'Electric'
    
    # Use str.contains to find rows where 'engine' contains 'Electric' (case-insensitive)
    # Only affect rows where 'fuel_type' is null
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Electric', case=False, na=False)), 'fuel_type'] = 'Electric'
    
    # Use str.contains to find rows where 'engine' contains 'Gasoline' (case-insensitive)
    # Only affect rows where 'fuel_type' is null
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Gasoline', case=False, na=False)), 'fuel_type'] = 'Gasoline'
    
    # Typically, the terms "Dual Motor" and 'Standard Range Battery'refer to electric vehicles
    # Fill 'fuel_type' with 'Electric' for cars with 'Dual Motor - Standard' or 'Standard Range Battery' in 'engine'
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Dual Motor - Standard|Standard Range Battery', case=False, na=False)), 'fuel_type'] = 'Electric'
    
    # Given the term "GDI" (Gasoline Direct Injection), it is safe to assume that engines with "GDI DOHC" are gasoline-powered vehicles.

    # Fill 'fuel_type' with 'Gasoline' for cars with 'GDI DOHC' in 'engine' and where 'fuel_type' is null
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('GDI DOHC', case=False, na=False)), 'fuel_type'] = 'Gasoline'
    
    # Fill 'fuel_type' for electric vehicles
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('120 AH|F-150 Lightning|Q4 e-tron|EV6', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for diesel engines
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Turbo Diesel', case=False, na=False)), 'fuel_type'] = 'Diesel'

    # Fill 'fuel_type' for gasoline turbo engines
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Twin Turbo', case=False, na=False)), 'fuel_type'] = 'Gasoline'
    
    # Fill 'fuel_type' for electric vehicles (F-150 Lightning, Kia EV6, Audi Q4 e-tron)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('F-150 Lightning|EV6|Q4 e-tron', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for gasoline vehicles (Nissan Kicks, Mercedes-Benz S-Class, Ford Air Pure, Audi Q5, Mercedes-Benz R-Class)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('Kicks|S-Class|Air Pure|Q5|R 350', case=False, na=False)), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'engine' is '4.0 Liter'
    df.loc[(df['fuel_type'].isnull()) & (df['engine'] == '4.0 Liter'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'engine' is '2.0 Liter'
    df.loc[(df['fuel_type'].isnull()) & (df['engine'] == '2.0 Liter'), 'fuel_type'] = 'Gasoline'

     # Fill missing 'fuel_type' values when 'engine' is 'V8'
    df.loc[(df['fuel_type'].isnull()) & (df['engine'] == 'V8'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'F-PACE S'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'F-PACE S'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Sonata Hybrid Limited'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Sonata Hybrid Limited'), 'fuel_type'] = 'Hybrid'

    # Fill missing 'fuel_type' values when 'model' is 'Niro EV EX'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Niro EV EX'), 'fuel_type'] = 'Electric'
    
     # Fill missing 'fuel_type' values when 'model' is 'e-tron Prestige'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'e-tron Prestige'), 'fuel_type'] = 'Electric'

    # Fill missing 'fuel_type' values when 'model' is '1500 Laramie'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == '1500 Laramie'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Hardtop Cooper'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Hardtop Cooper'), 'fuel_type'] = 'Gasoline' 

    # Fill missing 'fuel_type' values when 'model' is 'E-Class E 400 4MATIC'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'E-Class E 400 4MATIC'), 'fuel_type'] = 'Gasoline' 

    # Fill missing 'fuel_type' values when 'model' is 'bZ4X Limited	'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'bZ4X Limited'), 'fuel_type'] = 'Gasoline' 
    
    # Fill missing 'fuel_type' values when 'model' is 'Pacifica Launch Edition'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Pacifica Launch Edition'), 'fuel_type'] = 'Diesel' 

    # Fill missing 'fuel_type' values when 'model' is 'R1S Adventure Package'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'R1S Adventure Package'), 'fuel_type'] = 'Gasoline' 

    # Fill missing 'fuel_type' values when 'model' is 'MDX 3.5L w/Advance & Entertainment Pkgs'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'MDX 3.5L w/Advance & Entertainment Pkgs'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Bronco Sport Big Bend'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Bronco Sport Big Bend'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'A4 2.0T Premium'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'A4 2.0T Premium'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Titan SV'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Titan SV'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Charger GT'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Charger GT'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is 'Mustang Mach-E GT'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == 'Mustang Mach-E GT'), 'fuel_type'] = 'Gasoline'

    # Fill missing 'fuel_type' values when 'model' is '500e Battery Electric'
    df.loc[(df['fuel_type'].isnull()) & (df['model'] == '500e Battery Electric'), 'fuel_type'] = 'Electric'


    # drops all values where we couldnt find the fuel_type
    df.dropna(subset=['fuel_type'], inplace=True)
    
    #Fill 'clean_title' with 'None reported'
    #df.clean_title.fillna('None reported', inplace = True) - error in future version
    df['accident']= df['accident'].apply(lambda x:'None reported' if pd.isna(x) else x)

    #Fill 'accident' with 'No'
    # df.accident.fillna('No', inplace = True) -  error in future version
    df['clean_title']= df['clean_title'].apply(lambda x:'No' if pd.isna(x) else x)

    return df



def format_columns (df):

    # Group 'Plug-In Hybrid' with 'Hybrid' and 'E85 Flex Fuel' with 'Gasoline'
    df['fuel_type'] = df['fuel_type'].replace({
    'Plug-In Hybrid': 'Hybrid',
    'E85 Flex Fuel': 'Gasoline'
    })

    #Group transmission in smaller groups
    df['transmission'] = df['transmission'].apply(map_transmission)

    # change colors to have few values
    df = update_color(df, 'ext_col')
    df = update_color(df, 'int_col')

    return df
    


def map_transmission(trans):
    for key, values in transmission_mapping.items():
        if trans in values:
            return key
    return 'Other'

def update_color(df, col):
    df.loc[(df[col].str.contains('Black', case=False, na=False)), col] = 'Black'
    df.loc[(df[col].str.contains('Noir', case=False, na=False)), col] = 'Black'
    df.loc[(df[col].str.contains('Blue', case=False, na=False)), col] = 'Blue'
    df.loc[(df[col].str.contains('Blu', case=False, na=False)), col] = 'Blue'
    df.loc[(df[col].str.contains('Red', case=False, na=False)), col] = 'Red'
    df.loc[(df[col].str.contains('White', case=False, na=False)), col] = 'White'
    df.loc[(df[col].str.contains('Green', case=False, na=False)), col] = 'Green'
    df.loc[(df[col].str.contains('Gray', case=False, na=False)), col] = 'Gray'
    df.loc[(df[col].str.contains('Grey', case=False, na=False)), col] = 'Gray'
    df.loc[(df[col].str.contains('Silver', case=False, na=False)), col] = 'Silver'
    df.loc[(df[col].str.contains('Metallic', case=False, na=False)), col] = 'Metallic'
    df.loc[(df[col].str.contains('Yellow', case=False, na=False)), col] = 'Yellow'
    df.loc[(df[col].str.contains('Orange', case=False, na=False)), col] = 'Orange'
    df.loc[(df[col].str.contains('Brown', case=False, na=False)), col] = 'Brown'
    df.loc[(df[col].str.contains('Beige', case=False, na=False)), col] = 'Beige'
    colors = ['Black', 'Blue', 'Red','White','Green','Gray','Silver','Metallic','Gold','Brown','Orange','Beige','Yellow','Purple','Pink']

    # Use .str.contains() to create a mask for rows containing any word from words_list
    # We use '|'.join to create a regular expression that matches any word in words_list
    pattern = '|'.join(colors)
    mask = df[col].str.contains(pattern, case=False, regex=True)

    # Change the value if the text does NOT contain any word from the list
    df.loc[~mask, col] = 'Others'
    return df



#FORMATING AND DUMMIE CREATION FUNCTIONS


# extract HP, Liters and Cylinder
def extract_engine_info(engine, fuel_type):
        hp_search = re.search(r'(\d+(\.\d+)?)HP', engine)
        litre_search = re.search(r'(\d+(\.\d+)?)L', engine)
        cylinders_search = re.search(r'(\d+) Cylinder', engine)
        
        hp = float(hp_search.group(1)) if hp_search else ''
        litres = float(litre_search.group(1)) if litre_search else ''
        cylinders = int(cylinders_search.group(1)) if cylinders_search else ''

        
        return pd.Series([hp, litres, cylinders])




    
def creat_dummies (df):
    # creating automatic dummies
    
    dummies_fuel = pd.get_dummies(df[['id','fuel_type']], columns=['fuel_type'], drop_first=False)
    dummies_transm = pd.get_dummies(df[['id','transmission']], columns=['transmission'], drop_first=False)
    dummies_brand = pd.get_dummies(df[['id','brand']], columns=['brand'], drop_first=False)
    
    #creating manual dummies

    engine_info = df.apply(lambda row: extract_engine_info(row['engine'], row['fuel_type']), axis=1)
    df[['horsepower', 'engine_size', 'cylinders']] = engine_info

    #merging all into one df
    merged_df = pd.merge(df, dummies_fuel, on='id', how='left')
    merged_df = pd.merge(merged_df, dummies_transm, on='id', how='left')
    merged_df = pd.merge(merged_df, dummies_brand, on='id', how='left')

    #droping old columns that were transformed into dummies
    merged_df = merged_df.drop(['fuel_type','transmission','engine','brand'], axis = 1)

    # changing the values for 'clean_title' and 'accident' to true or false
    merged_df['clean_title']= merged_df['clean_title'].apply(lambda x: False if x == 'No' else True)
    merged_df['accident']= merged_df['accident'].apply(lambda x: False if x == 'None reported' else True)

    # coverting all boll to int for the test
    boolean_columns = merged_df.select_dtypes(include='bool').columns
    merged_df[boolean_columns] = merged_df[boolean_columns].astype(int)

    return merged_df
    

