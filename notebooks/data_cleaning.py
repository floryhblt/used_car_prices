#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def update_fuel_type(df):
    # Fill missing 'fuel_type' values when the model is 'Tesla'
    df.loc[(df['fuel_type'].isnull()) & (df['brand'] == 'Tesla'), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for electric vehicles
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Electric|120 AH|F-150 Lightning|Q4 e-tron|EV6|Dual Motor - Standard|Standard Range Battery', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for electric vehicles (F-150 Lightning, Kia EV6, Audi Q4 e-tron)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('F-150 Lightning|EV6|Q4 e-tron', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for gasoline vehicles
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Gasoline|Twin Turbo|GDI DOHC', case=False, na=False)), 'fuel_type'] = 'Gasoline'

    # Fill 'fuel_type' for gasoline vehicles (Nissan Kicks, Mercedes-Benz S-Class, Ford Air Pure, Audi Q5, Mercedes-Benz R-Class)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('Kicks|S-Class|Air Pure|Q5|R 350', case=False, na=False)), 'fuel_type'] = 'Gasoline'

    # Fill 'fuel_type' for diesel engines
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Turbo Diesel', case=False, na=False)), 'fuel_type'] = 'Diesel'
    
    return df


