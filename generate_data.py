import random
import csv
from datetime import datetime, timedelta

random.seed(42)

# Parameters
num_records = 7500
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

raw_customer_names = [
    'Aarav Sharma', 'Aditi Rao', 'Alexander Wright', 'Amanda Jones', 'Ananya Patel',
    'Andrew Miller', 'Benjamin Scott', 'Bhavna Joshi', 'Carlos Mendez', 'Catherine Davis',
    'Chloe Bennett', 'Daniel Evans', 'David Smith', 'Devendra Singh', 'Divya Nair',
    'Emily Clark', 'Emma Wilson', 'Ethan Taylor', 'Grace Thomas', 'Harish Kumar',
    'Henry White', 'Ishaan Verma', 'Jacob Harris', 'James Martin', 'Jessica Hall',
    'Jonathan Allen', 'Kavita Reddy', 'Liam Johnson', 'Lucas Anderson', 'Manish Gupta',
    'Marcus Robinson', 'Mia Walker', 'Michael Brown', 'Neha Kapoor', 'Noah Martinez',
    'Oliver Garcia', 'Pooja Iyer', 'Pranav Mukherjee', 'Priya Menon', 'Rahul Sen',
    'Rohan Mehra', 'Samantha King', 'Sanjay Dutt', 'Sarah Johnson', 'Sneha Roy',
    'Sophia Baker', 'Sunil Narang', 'Tanvi Saxena', 'Vikram Malhotra', 'William Lee'
]

customers = []
for i, name in enumerate(raw_customer_names * 6):
    seg = random.choices(['Consumer', 'Corporate', 'Home Office'], weights=[0.52, 0.30, 0.18])[0]
    customers.append((f'CUST-{1001 + i}', name, seg))

regions_data = [
    ('United States', 'California', 'Los Angeles', '90036', 'West'),
    ('United States', 'California', 'San Francisco', '94109', 'West'),
    ('United States', 'California', 'San Diego', '92154', 'West'),
    ('United States', 'Washington', 'Seattle', '98101', 'West'),
    ('United States', 'Washington', 'Spokane', '99201', 'West'),
    ('United States', 'New York', 'New York City', '10024', 'East'),
    ('United States', 'New York', 'Buffalo', '14215', 'East'),
    ('United States', 'Pennsylvania', 'Philadelphia', '19140', 'East'),
    ('United States', 'Massachusetts', 'Boston', '02116', 'East'),
    ('United States', 'Illinois', 'Chicago', '60653', 'Central'),
    ('United States', 'Texas', 'Houston', '77005', 'Central'),
    ('United States', 'Texas', 'Dallas', '75220', 'Central'),
    ('United States', 'Texas', 'Austin', '78701', 'Central'),
    ('United States', 'Michigan', 'Detroit', '48227', 'Central'),
    ('United States', 'Florida', 'Miami', '33180', 'South'),
    ('United States', 'Florida', 'Orlando', '32801', 'South'),
    ('United States', 'Georgia', 'Atlanta', '30318', 'South'),
    ('United States', 'North Carolina', 'Charlotte', '28205', 'South'),
    ('United States', 'Tennessee', 'Nashville', '37208', 'South')
]

products_catalog = [
    # Technology
    ('PROD-TEC-1001', 'Technology', 'Laptops', 'ProBook Elite 15.6 Laptop', 750.00, 1099.99),
    ('PROD-TEC-1002', 'Technology', 'Laptops', 'UltraSlim Touch Laptop 14', 580.00, 849.50),
    ('PROD-TEC-1003', 'Technology', 'Phones', 'Vision Smartphone 128GB', 390.00, 699.00),
    ('PROD-TEC-1004', 'Technology', 'Phones', 'Horizon Pro 5G Flagship', 520.00, 899.99),
    ('PROD-TEC-1005', 'Technology', 'Accessories', 'Wireless Noise-Canceling Headphones', 85.00, 179.99),
    ('PROD-TEC-1006', 'Technology', 'Accessories', 'Ergonomic Mechanical Keyboard', 45.00, 119.00),
    ('PROD-TEC-1007', 'Technology', 'Accessories', 'Fast Wireless Charging Dock', 18.00, 49.99),
    ('PROD-TEC-1008', 'Technology', 'Accessories', 'Ultra HD 4K Webcam w/ Mic', 35.00, 89.99),
    # Furniture
    ('PROD-FUR-2001', 'Furniture', 'Chairs', 'Executive Mesh High-Back Chair', 120.00, 249.99),
    ('PROD-FUR-2002', 'Furniture', 'Chairs', 'Ergonomic Task Swivel Chair', 70.00, 149.50),
    ('PROD-FUR-2003', 'Furniture', 'Tables', 'Electric Height-Adjustable Standing Desk', 210.00, 429.00),
    ('PROD-FUR-2004', 'Furniture', 'Tables', 'Solid Oak Conference Table', 450.00, 799.00),
    ('PROD-FUR-2005', 'Furniture', 'Bookcases', '5-Tier Modular Storage Bookcase', 80.00, 175.00),
    ('PROD-FUR-2006', 'Furniture', 'Bookcases', 'Modern Minimalist Wall Shelf Unit', 40.00, 95.00),
    ('PROD-FUR-2007', 'Furniture', 'Furnishings', 'Dimmable LED Desk Lamp w/ USB', 15.00, 42.00),
    # Office Supplies
    ('PROD-OFF-3001', 'Office Supplies', 'Storage', 'Heavy Duty 3-Drawer File Cabinet', 65.00, 139.99),
    ('PROD-OFF-3002', 'Office Supplies', 'Storage', 'Stackable Clear Document Bins 4-Pack', 12.00, 29.99),
    ('PROD-OFF-3003', 'Office Supplies', 'Binders', 'Heavy-Duty Ring Binder 2-Inch', 3.50, 9.99),
    ('PROD-OFF-3004', 'Office Supplies', 'Paper', 'Premium Multipurpose Copy Paper 5-Ream', 14.00, 32.50),
    ('PROD-OFF-3005', 'Office Supplies', 'Paper', 'Eco-Recycled Printer Paper Case', 18.00, 39.99),
    ('PROD-OFF-3006', 'Office Supplies', 'Appliances', 'Compact Office Coffee Brewer', 45.00, 99.00),
    ('PROD-OFF-3007', 'Office Supplies', 'Art', 'Professional Presentation Marker Set', 6.00, 18.50),
    ('PROD-OFF-3008', 'Office Supplies', 'Fasteners', 'Industrial Stapler & Heavy Staples Set', 8.50, 22.00),
    ('PROD-OFF-3009', 'Office Supplies', 'Envelopes', 'Self-Seal Security Envelopes Box 500', 7.00, 19.99)
]

ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
ship_weights = [0.60, 0.20, 0.15, 0.05]

discounts = [0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]

records = []
for i in range(1, num_records + 1):
    # Simulated order grouping: each order has 1 to 4 items
    order_id = f'SV-{(i // 3) + 10001}'
    day_offset = random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=day_offset)
    
    # Seasonality boost for Q4 (Nov, Dec)
    if order_date.month in [11, 12] and random.random() < 0.25:
        pass
        
    ship_delay = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[0.1, 0.15, 0.3, 0.25, 0.1, 0.07, 0.03])[0]
    ship_date = order_date + timedelta(days=ship_delay)
    ship_mode = random.choices(ship_modes, weights=ship_weights)[0]
    
    cust_id, cust_name, segment = random.choice(customers)
    country, state, city, postal_code, region = random.choice(regions_data)
    
    prod_id, category, subcat, prod_name, cost, price = random.choice(products_catalog)
    qty = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 10], weights=[0.35, 0.25, 0.15, 0.1, 0.06, 0.04, 0.02, 0.02, 0.01])[0]
    
    discount = random.choice(discounts)
    
    # Calculate Sales and Profit
    gross_sales = round(qty * price * (1 - discount), 2)
    total_cost = round(qty * cost, 2)
    profit = round(gross_sales - total_cost, 2)
    
    # Data Quality nuances to clean in Phase 2:
    # 1. Whitespace in customer name occasionally
    if i % 85 == 0:
        cust_name = f'  {cust_name} '
    # 2. Lowercase segment occasionally
    if i % 120 == 0:
        segment = segment.lower()
    # 3. Missing postal code occasionally
    if i % 150 == 0:
        postal_code = ''
    # 4. Inconsistent ship mode casing occasionally
    if i % 200 == 0:
        ship_mode = ship_mode.upper()
        
    records.append([
        f'ROW-{100000 + i}',
        order_id,
        order_date.strftime('%Y-%m-%d'),
        ship_date.strftime('%Y-%m-%d'),
        ship_mode,
        cust_id,
        cust_name,
        segment,
        country,
        city,
        state,
        postal_code,
        region,
        prod_id,
        category,
        subcat,
        prod_name,
        f'{cost:.2f}',
        f'{price:.2f}',
        qty,
        f'{discount:.2f}',
        f'{gross_sales:.2f}',
        f'{profit:.2f}'
    ])

# Add 15 deliberate duplicate rows for Phase 2 data cleaning exercise
for d in range(15):
    records.append(records[d * 50].copy())

headers = [
    'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
    'Customer ID', 'Customer Name', 'Segment', 'Country', 'City',
    'State', 'Postal Code', 'Region', 'Product ID', 'Category',
    'Sub-Category', 'Product Name', 'Unit Cost', 'Unit Price',
    'Quantity', 'Discount', 'Sales', 'Profit'
]

output_filename = 'SalesVision_Raw_Data.csv'
with open(output_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(records)

print(f'Successfully generated {len(records)} rows in {output_filename}')
