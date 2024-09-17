#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def update_fuel_type(df):
    # Fill missing 'fuel_type' values when the model is 'Tesla'
    df.loc[(df['fuel_type'].isnull()) & (df['brand'] == 'Tesla'), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for electric vehicles based on engine descriptions
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Electric|120 AH|F-150 Lightning|Q4 e-tron|EV6|Dual Motor - Standard|Standard Range Battery|Mach-E GT|Battery Electric|e-tron', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for electric vehicles based on model names (including new ones)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('F-150 Lightning|EV6|Q4 e-tron|Mach-E GT|R1S Adventure Package|bZ4X|500e|Niro EV|Revero|Cooper Electric', case=False, na=False)), 'fuel_type'] = 'Electric'

    # Fill 'fuel_type' for gasoline vehicles based on engine descriptions
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Gasoline|Twin Turbo|GDI DOHC|MPFI DOHC|V6|V8|PDI DOHC', case=False, na=False)), 'fuel_type'] = 'Gasoline'

    # Fill 'fuel_type' for gasoline vehicles based on model names (including new ones)
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('Kicks|S-Class|Air Pure|Q5|R 350|Titan|Charger|Sentra|Laramie|A4 2.0T|F-PACE', case=False, na=False)), 'fuel_type'] = 'Gasoline'

    # Fill 'fuel_type' for diesel engines based on the engine description
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Turbo Diesel|Diesel', case=False, na=False)), 'fuel_type'] = 'Diesel'

    # Fill 'fuel_type' for hybrid vehicles based on model names and engine descriptions
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('Sonata Hybrid|Hybrid', case=False, na=False)), 'fuel_type'] = 'Hybrid'

    # Fill 'fuel_type' for hybrid vehicles based on engine descriptions
    df.loc[(df['fuel_type'].isnull()) & (df['engine'].str.contains('Hybrid|Plug-In Hybrid', case=False, na=False)), 'fuel_type'] = 'Hybrid'
    
    # Specific logic based on known patterns in remaining NaNs (e.g., based on a unique pattern in engine, brand, or model)
    df.loc[(df['fuel_type'].isnull()) & (df['brand'] == 'Mercedes-Benz') & (df['engine'].str.contains('3.0 Liter', case=False, na=False)), 'fuel_type'] = 'Gasoline'
    
    # Add logic based on model name patterns
    df.loc[(df['fuel_type'].isnull()) & (df['model'].str.contains('Hardtop Cooper', case=False, na=False)), 'fuel_type'] = 'Gasoline'
    
    # Handle Volkswagen e-tron with electric engine
    df.loc[(df['fuel_type'].isnull()) & (df['brand'] == 'Volkswagen') & (df['engine'].str.contains('111.2Ah', case=False, na=False)), 'fuel_type'] = 'Electric'
    
    return df
