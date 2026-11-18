# SalesVision – Sales Performance & Business Intelligence Dashboard
## Phase 1: Project Planning & Data Architecture Document

### 1. Project Overview & Business Problem Statement
Modern enterprises generate massive volumes of transactional sales data every day. However, executive management and sales leadership frequently encounter significant hurdles:
- **Lack of Centralized Visibility**: Data sits in transactional silos (ERP/CRM/flat files), making it difficult to assess overall company performance in real time.
- **Profitability Leaks**: High sales volume often disguises margin losses caused by deep unmonitored discounting, unprofitable product sub-categories, or high regional logistics costs.
- **Delayed Strategic Decision-Making**: Inability to quickly track Year-over-Year (YoY) revenue changes, customer segment profitability, and regional disparities prevents agile inventory and marketing decisions.

**Project Objective:**
Design and deploy an end-to-end Power BI executive business intelligence solution that consolidates multi-year sales data, calculates vital business metrics using DAX, and delivers interactive, intuitive dashboards to empower stakeholders with data-driven decision-making.

---

### 2. Business Requirements Document (BRD)
| Requirement ID | Category | Business Requirement Description |
| :--- | :--- | :--- |
| **BR-01** | Executive KPIs | Real-time tracking of Total Sales, Total Profit, Profit Margin %, Total Orders, Total Units Sold, and Average Order Value (AOV). |
| **BR-02** | Time Intelligence | Comparison of sales against Previous Year (YoY Sales Growth %) and Year-to-Date (YTD) cumulative performance. |
| **BR-03** | Product Performance | Identification of Top 10 revenue-generating products, bottom underperformers, and category/sub-category margin breakdowns. |
| **BR-04** | Regional Performance | Geographic sales and profit distribution across Territories/Regions, States, and Cities to spotlight high-margin vs loss-making areas. |
| **BR-05** | Customer Intelligence | Sales and profitability analysis by Customer Segment (Consumer, Corporate, Home Office) and customer purchase frequency. |
| **BR-06** | Interactive Exploration | Dynamic slicing by Date, Category, Region, and Segment with seamless drill-down and drill-through capabilities. |

---

### 3. Dataset Architecture & Data Dictionary
The raw dataset is stored in `SalesVision_Raw_Data.csv` (7,515 records spanning 2023–2025).

| Column Name | Data Type | Sample Value | Role / Key Type | Business Description |
| :--- | :--- | :--- | :--- | :--- |
| **Row ID** | Integer / Text | `ROW-100001` | Technical Surrogate Key | Unique row-level identifier for the transactional export. |
| **Order ID** | Text | `SV-10001` | Transaction Header Key | Unique sales order identifier. One order may have multiple product line items. |
| **Order Date** | Date | `2023-11-02` | Foreign Key (Calendar) | Date when the customer placed the order. |
| **Ship Date** | Date | `2023-11-06` | Date | Date when the shipment was dispatched. |
| **Ship Mode** | Text | `Standard Class` | Dimension Attribute | Shipping tier (`Standard Class`, `Second Class`, `First Class`, `Same Day`). |
| **Customer ID** | Text | `CUST-1001` | Foreign Key (Customer) | Unique identifier for each customer. |
| **Customer Name**| Text | `Jonathan Allen` | Dimension Attribute | Full name of the customer. |
| **Segment** | Text | `Consumer` | Dimension Attribute | Market segment (`Consumer`, `Corporate`, `Home Office`). |
| **Country** | Text | `United States` | Dimension Attribute | Nation where transaction occurred. |
| **City** | Text | `New York City` | Dimension Attribute | City of delivery. |
| **State** | Text | `New York` | Dimension Attribute | State/Province of delivery. |
| **Postal Code** | Text | `10024` | Dimension Attribute | ZIP/Postal code for geospatial analysis. |
| **Region** | Text | `East` | Dimension Attribute | Sales territory (`East`, `West`, `Central`, `South`). |
| **Product ID** | Text | `PROD-TEC-1001` | Foreign Key (Product) | Unique identifier for each product SKU. |
| **Category** | Text | `Technology` | Dimension Attribute | High-level product category (`Technology`, `Furniture`, `Office Supplies`). |
| **Sub-Category**| Text | `Laptops` | Dimension Attribute | Specific product sub-classification. |
| **Product Name**| Text | `ProBook Elite 15.6 Laptop` | Dimension Attribute | Descriptive commercial name of the item. |
| **Unit Cost** | Decimal Number | `750.00` | Fact Metric | Cost of Goods Sold (COGS) per unit. |
| **Unit Price** | Decimal Number | `1099.99` | Fact Metric | Base retail price per unit before discounts. |
| **Quantity** | Whole Number | `2` | Fact Metric | Quantity of units purchased in this order line item. |
| **Discount** | Decimal / Percentage | `0.10` | Fact Metric | Percentage discount applied (0.00 to 0.50). |
| **Sales** | Decimal Number | `1979.98` | Fact Metric | Net revenue: `Quantity * Unit Price * (1 - Discount)`. |
| **Profit** | Decimal Number | `479.98` | Fact Metric | Net profit: `Sales - (Quantity * Unit Cost)`. |

---

### 4. Conceptual Data Model (Star Schema Preview)
To adhere to enterprise data modeling standards (Kimball dimensional modeling), the flat transactional dataset will be transformed into a **Star Schema** in Phase 2 and Phase 3:

```
           +---------------------+
           |    Dim_Calendar     |
           |  (Date Dimension)   |
           +----------+----------+
                      | 1
                      |
                      | *
+-----------------+   |   +-----------------+
|  Dim_Customers  |---*---|   Fact_Orders   |---*---|  Dim_Products   |
| (1:Many on      | 1   * | (Line Item Fact)| *   1 | (1:Many on      |
|  Customer ID)   |       |   Table)        |       |  Product ID)    |
+-----------------+       +--------+--------+       +-----------------+
                                   | *
                                   |
                                   | 1
                          +--------+--------+
                          |   Dim_Geography |
                          |   (1:Many on    |
                          |    Region/City) |
                          +-----------------+
```

- **Fact Table (`Fact_Orders`)**: Stores numeric transactional facts and metrics (`Sales`, `Profit`, `Quantity`, `Discount`, `Unit Cost`, `Unit Price`) along with foreign keys.
- **Dimension Tables**:
  - `Dim_Customers`: Customer ID (PK), Customer Name, Segment.
  - `Dim_Products`: Product ID (PK), Product Name, Category, Sub-Category.
  - `Dim_Geography`: Postal Code / City / State / Region.
  - `Dim_Calendar`: Date (PK), Year, Quarter, Month Name, Month Number, Day, Weekday, Year-Month.
