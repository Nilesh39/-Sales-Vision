import pandas as pd

# Load the clean dataset
df = pd.read_csv('SalesVision_Cleaned_Data.csv')

# 1. Dim_Customers
dim_customers = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates().sort_values('Customer ID')
print(f"Dim_Customers: {len(dim_customers)} unique customers. Unique PK? {dim_customers['Customer ID'].is_unique}")
dim_customers.to_csv('Dim_Customers.csv', index=False)

# 2. Dim_Products
dim_products = df[['Product ID', 'Product Name', 'Category', 'Sub-Category', 'Unit Cost', 'Unit Price']].drop_duplicates(subset=['Product ID']).sort_values('Product ID')
print(f"Dim_Products: {len(dim_products)} unique products. Unique PK? {dim_products['Product ID'].is_unique}")
dim_products.to_csv('Dim_Products.csv', index=False)

# 3. Dim_Geography
dim_geography = df[['Postal Code', 'City', 'State', 'Region', 'Country']].drop_duplicates(subset=['Postal Code']).sort_values('Postal Code')
print(f"Dim_Geography: {len(dim_geography)} unique postal areas. Unique PK? {dim_geography['Postal Code'].is_unique}")
dim_geography.to_csv('Dim_Geography.csv', index=False)

# 4. Fact_Orders
fact_orders = df[[
    'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
    'Customer ID', 'Product ID', 'Postal Code',
    'Quantity', 'Discount', 'Sales', 'Profit', 'Shipping Days', 'Line Margin %'
]].copy()
print(f"Fact_Orders: {len(fact_orders)} line items. Unique Row ID? {fact_orders['Row ID'].is_unique}")
fact_orders.to_csv('Fact_Orders.csv', index=False)

print("\nSuccessfully generated normalized Star Schema CSV files!")
