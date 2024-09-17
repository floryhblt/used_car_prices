#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def update_fuel_type(df):
    df.loc[df['engine'].str.contains('Electric', case=False, na=False), 'fuel_type'] = 'Electric'
    df.loc[df['engine'].str.contains('Gasoline', case=False, na=False), 'fuel_type'] = 'Gasoline'
    df.loc[(df['brand'].str.lower() == 'tesla') & (df['engine'].str.contains('Dual Motor - Standard', case=False, na=False)), 'fuel_type'] = 'Electric'    
    
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

    return df

