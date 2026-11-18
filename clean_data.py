import pandas as pd
import numpy as np

# Load raw dataset
raw_path = 'SalesVision_Raw_Data.csv'
df = pd.read_csv(raw_path)

print("--- RAW DATA AUDIT ---")
print(f"Total Rows: {len(df)}")
print(f"Duplicate Rows Count: {df.duplicated().sum()}")
print(f"Unique Segments (dirty): {df['Segment'].unique().tolist()}")
print(f"Unique Ship Modes (dirty): {df['Ship Mode'].unique().tolist()}")
print(f"Blank Postal Codes: {df['Postal Code'].isna().sum() + (df['Postal Code'] == '').sum()}")

# STEP 1: Remove Duplicates
df_cleaned = df.drop_duplicates().copy()

# STEP 2: Text Cleaning & Standardization
# Trim whitespace
df_cleaned['Customer Name'] = df_cleaned['Customer Name'].str.strip()
# Title Case for Segment and Ship Mode
df_cleaned['Segment'] = df_cleaned['Segment'].str.strip().str.title()
df_cleaned['Ship Mode'] = df_cleaned['Ship Mode'].str.strip().str.title()

# STEP 3: Handle Missing Values
# Map postal codes by City if missing, or default
city_postal_map = {
    'Los Angeles': '90036', 'San Francisco': '94109', 'San Diego': '92154',
    'Seattle': '98101', 'Spokane': '99201', 'New York City': '10024',
    'Buffalo': '14215', 'Philadelphia': '19140', 'Boston': '02116',
    'Chicago': '60653', 'Houston': '77005', 'Dallas': '75220',
    'Austin': '78701', 'Detroit': '48227', 'Miami': '33180',
    'Orlando': '32801', 'Atlanta': '30318', 'Charlotte': '28205',
    'Nashville': '37208'
}

def fill_postal(row):
    val = str(row['Postal Code']).strip()
    if val == '' or val == 'nan':
        return city_postal_map.get(row['City'], '99999')
    return val

df_cleaned['Postal Code'] = df_cleaned.apply(fill_postal, axis=1)

# STEP 4: Correct Data Types
df_cleaned['Order Date'] = pd.to_datetime(df_cleaned['Order Date'])
df_cleaned['Ship Date'] = pd.to_datetime(df_cleaned['Ship Date'])
df_cleaned['Unit Cost'] = df_cleaned['Unit Cost'].astype(float)
df_cleaned['Unit Price'] = df_cleaned['Unit Price'].astype(float)
df_cleaned['Quantity'] = df_cleaned['Quantity'].astype(int)
df_cleaned['Discount'] = df_cleaned['Discount'].astype(float)
df_cleaned['Sales'] = df_cleaned['Sales'].astype(float)
df_cleaned['Profit'] = df_cleaned['Profit'].astype(float)

# STEP 5: Create Calculated Columns
# 1. Shipping Days (Fulfillment Lead Time)
df_cleaned['Shipping Days'] = (df_cleaned['Ship Date'] - df_cleaned['Order Date']).dt.days

# 2. Line Profit Margin %
df_cleaned['Line Margin %'] = np.where(df_cleaned['Sales'] > 0, (df_cleaned['Profit'] / df_cleaned['Sales']) * 100, 0.0)
df_cleaned['Line Margin %'] = df_cleaned['Line Margin %'].round(2)

# Format dates back to standard ISO YYYY-MM-DD for clean CSV export
df_cleaned['Order Date'] = df_cleaned['Order Date'].dt.strftime('%Y-%m-%d')
df_cleaned['Ship Date'] = df_cleaned['Ship Date'].dt.strftime('%Y-%m-%d')

output_path = 'SalesVision_Cleaned_Data.csv'
df_cleaned.to_csv(output_path, index=False)

print("\n--- CLEANED DATA AUDIT ---")
print(f"Total Clean Rows: {len(df_cleaned)}")
print(f"Duplicate Rows Count: {df_cleaned.duplicated().sum()}")
print(f"Unique Segments (clean): {df_cleaned['Segment'].unique().tolist()}")
print(f"Unique Ship Modes (clean): {df_cleaned['Ship Mode'].unique().tolist()}")
print(f"Blank Postal Codes: {df_cleaned['Postal Code'].isna().sum() + (df_cleaned['Postal Code'] == '').sum()}")
print(f"Average Shipping Days: {df_cleaned['Shipping Days'].mean():.2f} days")
print(f"Total Clean Sales: ${df_cleaned['Sales'].sum():,.2f}")
print(f"Total Clean Profit: ${df_cleaned['Profit'].sum():,.2f}")
