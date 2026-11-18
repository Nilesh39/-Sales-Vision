import pandas as pd
import numpy as np

# Load fact and dimensions
fact = pd.read_csv('Fact_Orders.csv')
prod = pd.read_csv('Dim_Products.csv')
fact['Order Date'] = pd.to_datetime(fact['Order Date'])
fact['Year'] = fact['Order Date'].dt.year
fact['Month'] = fact['Order Date'].dt.month
fact['YearMonth'] = fact['Order Date'].dt.strftime('%Y-%m')

total_sales = fact['Sales'].sum()
total_profit = fact['Profit'].sum()
total_orders = fact['Order ID'].nunique()
total_quantity = fact['Quantity'].sum()
aov = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Quantity: {total_quantity:,}")
print(f"Average Order Value: ${aov:,.2f}")
print(f"Overall Profit Margin %: {profit_margin:.2f}%")

# Yearly Breakdown & YoY
yearly = fact.groupby('Year').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique')
).reset_index()
yearly['PY_Sales'] = yearly['Sales'].shift(1)
yearly['YoY_Sales_Growth_%'] = ((yearly['Sales'] - yearly['PY_Sales']) / yearly['PY_Sales']) * 100
print("\n--- YEARLY TIME INTELLIGENCE AUDIT ---")
print(yearly.to_string(index=False))

# Merge with Dim_Products for Top 10 Products
merged = fact.merge(prod, on='Product ID')
top10 = merged.groupby('Product Name').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Quantity=('Quantity', 'sum')
).sort_values('Sales', ascending=False).head(10).reset_index()

print("\n--- TOP 10 PRODUCTS BY SALES ---")
print(top10.to_string(index=False))
