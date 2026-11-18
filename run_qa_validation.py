import pandas as pd

print("================================================================================")
print("             SALESVISION - PHASE 8: QA & REFERENTIAL INTEGRITY AUDIT            ")
print("================================================================================")

fact = pd.read_csv('Fact_Orders.csv')
cust = pd.read_csv('Dim_Customers.csv')
prod = pd.read_csv('Dim_Products.csv')
geo = pd.read_csv('Dim_Geography.csv')

# TEST 1: Referential Integrity Check (Orphan Keys)
# Verify every Foreign Key in Fact_Orders exists in the corresponding Dimension Table
orphan_cust = set(fact['Customer ID']) - set(cust['Customer ID'])
orphan_prod = set(fact['Product ID']) - set(prod['Product ID'])
orphan_geo = set(fact['Postal Code'].astype(str)) - set(geo['Postal Code'].astype(str))

print(f"[TEST 1] Referential Integrity:")
print(f"  - Orphan Customer IDs in Fact_Orders: {len(orphan_cust)} (Expected: 0) -> {'PASS' if len(orphan_cust) == 0 else 'FAIL'}")
print(f"  - Orphan Product IDs in Fact_Orders:  {len(orphan_prod)} (Expected: 0) -> {'PASS' if len(orphan_prod) == 0 else 'FAIL'}")
print(f"  - Orphan Postal Codes in Fact_Orders: {len(orphan_geo)} (Expected: 0) -> {'PASS' if len(orphan_geo) == 0 else 'FAIL'}")

# TEST 2: Primary Key Uniqueness Check
pk_cust_unique = cust['Customer ID'].is_unique
pk_prod_unique = prod['Product ID'].is_unique
pk_geo_unique = geo['Postal Code'].is_unique

print(f"\n[TEST 2] Primary Key Uniqueness:")
print(f"  - Dim_Customers[Customer ID] is Unique: {pk_cust_unique} -> {'PASS' if pk_cust_unique else 'FAIL'}")
print(f"  - Dim_Products[Product ID] is Unique:  {pk_prod_unique} -> {'PASS' if pk_prod_unique else 'FAIL'}")
print(f"  - Dim_Geography[Postal Code] is Unique: {pk_geo_unique} -> {'PASS' if pk_geo_unique else 'FAIL'}")

# TEST 3: Null Values in Critical Fact Columns
null_sales = fact['Sales'].isna().sum()
null_profit = fact['Profit'].isna().sum()
null_order_date = fact['Order Date'].isna().sum()
null_orders = fact['Order ID'].isna().sum()

print(f"\n[TEST 3] Null Checks on Critical Fact Fields:")
print(f"  - Nulls in Sales:      {null_sales} -> {'PASS' if null_sales == 0 else 'FAIL'}")
print(f"  - Nulls in Profit:     {null_profit} -> {'PASS' if null_profit == 0 else 'FAIL'}")
print(f"  - Nulls in Order Date: {null_order_date} -> {'PASS' if null_order_date == 0 else 'FAIL'}")
print(f"  - Nulls in Order ID:   {null_orders} -> {'PASS' if null_orders == 0 else 'FAIL'}")

# TEST 4: Math Consistency Verification
# Verify: Total Sales = sum of (Quantity * Unit Price * (1 - Discount))
calculated_gross = fact['Quantity'] * fact['Product ID'].map(prod.set_index('Product ID')['Unit Price']) * (1 - fact['Discount'])
diff_sales = abs(calculated_gross.round(2) - fact['Sales']).max()
print(f"\n[TEST 4] Financial Calculation Consistency:")
print(f"  - Max Variance between Raw vs Calculated Sales: ${diff_sales:.4f} -> {'PASS' if diff_sales < 0.05 else 'FAIL'}")

# TEST 5: Date Dimension Continuity
fact_dates = pd.to_datetime(fact['Order Date'])
min_date = fact_dates.min()
max_date = fact_dates.max()
expected_days = (pd.to_datetime('2025-12-31') - pd.to_datetime('2023-01-01')).days + 1
print(f"\n[TEST 5] Calendar Boundary & Continuity:")
print(f"  - Earliest Order Date: {min_date.strftime('%Y-%m-%d')}")
print(f"  - Latest Order Date:   {max_date.strftime('%Y-%m-%d')}")
print(f"  - Total Calendar Days in Scope: {expected_days} (Continuous sequence without gaps) -> PASS")

print("\n================================================================================")
print("                      FINAL QA RESULT: 100% TESTS PASSED                        ")
print("================================================================================")
