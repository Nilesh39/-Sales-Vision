import pandas as pd
import numpy as np

# Load tables
fact = pd.read_csv('Fact_Orders.csv')
prod = pd.read_csv('Dim_Products.csv')
cust = pd.read_csv('Dim_Customers.csv')
geo = pd.read_csv('Dim_Geography.csv')

# Merge
df = fact.merge(prod, on='Product ID').merge(cust, on='Customer ID').merge(geo, on='Postal Code')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month_Name'] = df['Order Date'].dt.strftime('%B')

print("=== 1. PRODUCT PERFORMANCE ===")
prod_agg = df.groupby(['Category', 'Sub-Category', 'Product Name']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Qty=('Quantity', 'sum'),
    Orders=('Order ID', 'nunique')
).reset_index()
prod_agg['Margin_%'] = (prod_agg['Profit'] / prod_agg['Sales']) * 100

print("--- Top 5 by Revenue ---")
print(prod_agg.sort_values('Sales', ascending=False).head(5)[['Product Name', 'Category', 'Sales', 'Profit', 'Margin_%']].to_string(index=False))

print("\n--- Bottom 5 by Profit Margin ---")
print(prod_agg.sort_values('Margin_%', ascending=True).head(5)[['Product Name', 'Category', 'Sales', 'Profit', 'Margin_%']].to_string(index=False))

print("\n=== 2. REGIONAL PERFORMANCE ===")
reg_agg = df.groupby('Region').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Qty=('Quantity', 'sum'),
    Orders=('Order ID', 'nunique'),
    Avg_Ship_Days=('Shipping Days', 'mean')
).reset_index()
reg_agg['Margin_%'] = (reg_agg['Profit'] / reg_agg['Sales']) * 100
reg_agg['Sales_Share_%'] = (reg_agg['Sales'] / df['Sales'].sum()) * 100
print(reg_agg.sort_values('Sales', ascending=False).to_string(index=False))

print("\n=== 3. MONTHLY SALES & SEASONALITY ===")
monthly_agg = df.groupby(['Month', 'Month_Name']).agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).reset_index().sort_values('Month')
monthly_agg['Margin_%'] = (monthly_agg['Profit'] / monthly_agg['Sales']) * 100
monthly_agg['Sales_Share_%'] = (monthly_agg['Sales'] / df['Sales'].sum()) * 100
print(monthly_agg[['Month_Name', 'Sales', 'Profit', 'Margin_%', 'Sales_Share_%']].to_string(index=False))

print("\n=== 4. DISCOUNTING IMPACT & MARGIN EROSION ===")
disc_agg = df.groupby('Discount').agg(
    Orders=('Order ID', 'count'),
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum')
).reset_index()
disc_agg['Margin_%'] = (disc_agg['Profit'] / disc_agg['Sales']) * 100
print(disc_agg.to_string(index=False))

print("\n=== 5. CUSTOMER SEGMENTS ===")
seg_agg = df.groupby('Segment').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Customers=('Customer ID', 'nunique')
).reset_index()
seg_agg['Margin_%'] = (seg_agg['Profit'] / seg_agg['Sales']) * 100
seg_agg['AOV'] = seg_agg['Sales'] / seg_agg['Orders']
seg_agg['Sales_Share_%'] = (seg_agg['Sales'] / df['Sales'].sum()) * 100
print(seg_agg.to_string(index=False))
