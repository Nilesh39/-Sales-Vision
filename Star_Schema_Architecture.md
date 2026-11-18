# SalesVision – Star Schema Data Model Architecture
## Phase 3: Dimensional Modeling Documentation

### 1. Conceptual & Physical Architecture (Star Schema)

```
                       +----------------------------------+
                       |           Dim_Calendar           |
                       |----------------------------------|
                       | [PK] Date                        |
                       |      Year                        |
                       |      Quarter                     |
                       |      Month Number                |
                       |      Month Name                  |
                       |      Month Short (Sorted by Num) |
                       |      Year-Month                  |
                       |      Day of Week                 |
                       +-----------------+----------------+
                                         | 1
                                         |
                                         | * (Active: Order Date)
                                         | : (Inactive: Ship Date)
+------------------------+               |               +------------------------+
|     Dim_Customers      | 1           * | *           1 |      Dim_Products      |
|------------------------|---------------+---------------|------------------------|
| [PK] Customer ID       |                               | [PK] Product ID        |
|      Customer Name     |                               |      Product Name      |
|      Segment           |                               |      Category          |
+------------------------+               |               |      Sub-Category      |
                                         |               |      Unit Cost         |
                                         | *             |      Unit Price        |
                                         |               +------------------------+
                                         | 1
                         +---------------+----------------+
                         |          Dim_Geography         |
                         |--------------------------------|
                         | [PK] Postal Code               |
                         |      City                      |
                         |      State                     |
                         |      Region                    |
                         |      Country                   |
                         +--------------------------------+
```

---

### 2. Table Specifications

#### A. Central Fact Table: `Fact_Orders`
- **Grain**: 1 row = 1 line item within a customer order.
- **Record Count**: 7,500 rows.
- **Foreign Keys**:
  - `Customer ID` $\rightarrow$ links to `Dim_Customers[Customer ID]`
  - `Product ID` $\rightarrow$ links to `Dim_Products[Product ID]`
  - `Postal Code` $\rightarrow$ links to `Dim_Geography[Postal Code]`
  - `Order Date` $\rightarrow$ links to `Dim_Calendar[Date]` (Active)
  - `Ship Date` $\rightarrow$ links to `Dim_Calendar[Date]` (Inactive, activated via `USERELATIONSHIP()`)
- **Measures / Numeric Facts**:
  - `Quantity`
  - `Discount`
  - `Sales`
  - `Profit`
  - `Shipping Days`
  - `Line Margin %`

#### B. Dimension Tables
1. **`Dim_Customers`** (300 unique rows)
   - Primary Key: `Customer ID` (Unique: Yes)
   - Attributes: `Customer Name`, `Segment`
2. **`Dim_Products`** (24 unique rows)
   - Primary Key: `Product ID` (Unique: Yes)
   - Attributes: `Product Name`, `Category`, `Sub-Category`, `Unit Cost`, `Unit Price`
3. **`Dim_Geography`** (19 unique rows)
   - Primary Key: `Postal Code` (Unique: Yes)
   - Attributes: `City`, `State`, `Region`, `Country`
4. **`Dim_Calendar`** (1,096 continuous rows spanning 2023-01-01 to 2025-12-31)
   - Primary Key: `Date` (Unique: Yes, continuous daily sequence)
   - Attributes: `Year`, `Quarter`, `Month Name`, `Month Short`, `Year-Month`, etc.

---

### 3. Model Relationships Summary

| From (Fact Table & FK) | To (Dimension Table & PK) | Cardinality | Cross Filter Direction | Status |
| :--- | :--- | :--- | :--- | :--- |
| `Fact_Orders[Customer ID]` | `Dim_Customers[Customer ID]` | Many to One (`*:1`) | Single | Active |
| `Fact_Orders[Product ID]` | `Dim_Products[Product ID]` | Many to One (`*:1`) | Single | Active |
| `Fact_Orders[Postal Code]` | `Dim_Geography[Postal Code]` | Many to One (`*:1`) | Single | Active |
| `Fact_Orders[Order Date]` | `Dim_Calendar[Date]` | Many to One (`*:1`) | Single | Active |
| `Fact_Orders[Ship Date]` | `Dim_Calendar[Date]` | Many to One (`*:1`) | Single | Inactive |

---

### 4. Enterprise Optimization Best Practices Implemented
1. **Star Schema vs. Snowflake**: We chose a pure Star Schema over Snowflake. Dim_Geography and Dim_Products are denormalized flat tables. This minimizes table joins and maximizes VertiPaq engine caching speed.
2. **Single-Direction Filtering**: All relationships filter from Dimension (1) to Fact (*). No bidirectional filters are permitted, preventing ambiguous filter paths and severe DAX slowdowns.
3. **Hide Foreign Keys in Fact Table**: In the Model View, right-click `Customer ID`, `Product ID`, and `Postal Code` in `Fact_Orders` and select **Hide in Report View**. This forces end-users and visual builders to slice only using dimension tables, ensuring clean filter propagation.
4. **Sort by Column**: Text attributes like `Month Short` ("Jan", "Feb") are explicitly sorted by `Month Number` (1, 2) rather than alphabetical order.
5. **Mark as Date Table**: Ensures Power BI turns off invisible auto-date-time hierarchy tables, saving RAM and enabling standard Time Intelligence functions.
