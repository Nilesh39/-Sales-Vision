# SalesVision – Sales Performance & Business Intelligence Dashboard

[![Power BI](https://img.shields.io/badge/Power_BI-Desktop_%26_Service-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![DAX](https://img.shields.io/badge/DAX-Advanced_Time_Intelligence-blue?logo=microsoft)](https://learn.microsoft.com/en-us/dax/)
[![Power Query](https://img.shields.io/badge/Power_Query-M_Language_ETL-orange)](https://learn.microsoft.com/en-us/power-query/)
[![Data Model](https://img.shields.io/badge/Architecture-Star_Schema-green)](https://en.wikipedia.org/wiki/Star_schema)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SalesVision** is an end-to-end, enterprise-grade Power BI business intelligence solution designed to analyze multi-year retail and commercial sales performance ($4.49M in revenue across 7,500 transactions). It empowers C-suite executives, sales directors, and regional managers to uncover profitability leaks, track customer lifetime value, evaluate regional growth velocity, and make data-driven pricing and inventory decisions.

---

## 📌 Table of Contents
1. [Business Problem & Objectives](#-business-problem--objectives)
2. [Solution Architecture](#-solution-architecture)
3. [Dimensional Modeling (Star Schema)](#-dimensional-modeling-star-schema)
4. [Data Cleaning Pipeline (Power Query)](#-data-cleaning-pipeline-power-query)
5. [DAX Measures Calculation Engine](#-dax-measures-calculation-engine)
6. [Interactive Dashboard Suite (5 Pages)](#-interactive-dashboard-suite-5-pages)
7. [Advanced Power BI Features](#-advanced-power-bi-features)
8. [Key Business Insights & Strategic ROI](#-key-business-insights--strategic-roi)
9. [Project Setup & Local Replication](#-project-setup--local-replication)
10. [Author & Resume Profile](#-author--resume-profile)

---

## 🎯 Business Problem & Objectives

### The Business Challenge
A growing enterprise operating across four major territories (**West, East, Central, South**) faced critical operational blind spots:
- **Disguised Margin Losses**: Strong top-line revenue ($4.49M) masked acute margin erosion caused by unmonitored promotional markdowns.
- **Geographic Imbalances**: Inability to identify whether low-volume regions like the East were unprofitable or simply underpenetrated.
- **Data Latency**: Relying on static, siloed operational spreadsheets prevented agile inventory allocation ahead of seasonal surges.

### Core Objectives
1. Build an automated **ETL pipeline** in Power Query to ingest and standardize messy operational records.
2. Design an optimized **Star Schema** with zero circular dependencies or bidirectional filters.
3. Engineer a comprehensive **DAX analytical engine** for Time Intelligence (YoY growth, YTD curves, AOV, and margin percentages).
4. Deliver a publication-grade, interactive 5-page dashboard with custom tooltips, drill-through diagnostics, and dynamic titles.
5. Provide actionable strategic recommendations that directly reclaim lost operating profit.

---

## 🏗 Solution Architecture

```
[ Raw CSV Data Export ] (7,515 Rows)
         |
         v
[ Power Query ETL Engine (M) ] -> Deduplication, Text Trimming, Proper Casing, Data Typing
         |
         v
[ Kimball Star Schema ]
   ├── Dim_Customers (300 Unique Entities)
   ├── Dim_Products (24 Product SKUs across 3 Categories)
   ├── Dim_Geography (19 Strategic Metros)
   ├── Dim_Calendar (1,096 Daily Records | Continuous DAX Table)
   └── Fact_Orders (7,500 Transaction Lines)
         |
         v
[ High-Performance DAX Calculation Engine ] -> 16 Production Measures in _Measures Table
         |
         v
[ Interactive Multi-Page Report Suite ]
   ├── 1. Executive Overview
   ├── 2. Sales Trends & Time Intelligence
   ├── 3. Product Performance & Profitability
   ├── 4. Regional Performance & Territory Mapping
   └── 5. Customer Analysis & Segment Economics
```

---

## 📐 Dimensional Modeling (Star Schema)

The data model follows strict **Kimball Dimensional Modeling** best practices:

```
                       +----------------------------------+
                       |           Dim_Calendar           |
                       |----------------------------------|
                       | [PK] Date                        |
                       |      Year, Quarter, Month, etc.  |
                       +-----------------+----------------+
                                         | 1
                                         |
                                         | * (Active: Order Date)
                                         | : (Inactive: Ship Date)
+------------------------+               |               +------------------------+
|     Dim_Customers      | 1           * | *           1 |      Dim_Products      |
|------------------------|---------------+---------------|------------------------|
| [PK] Customer ID       |          Fact_Orders          | [PK] Product ID        |
|      Customer Name     |-------------------------------|      Product Name      |
|      Segment           | [FK] Order Date               |      Category          |
+------------------------+ | [FK] Customer ID              |      Sub-Category      |
                           | [FK] Product ID               |      Unit Cost         |
                           | [FK] Postal Code              |      Unit Price        |
                           |      Sales, Profit, Quantity  | +------------------------+
                           +---------------+---------------+
                                           | *
                                           |
                                           | 1
                           +---------------+----------------+
                           |          Dim_Geography         |
                           |--------------------------------|
                           | [PK] Postal Code               |
                           |      City, State, Region       |
                           +--------------------------------+
```

### Relational Integrity & Optimization
- **Cardinality**: Strictly 1-to-Many (`1:*`) relationships.
- **Filter Direction**: Single-directional (Dimension $\rightarrow$ Fact) to prevent ambiguous filter paths.
- **VertiPaq Memory Optimization**: Fact table foreign keys are hidden from report view; auto date/time is disabled.

---

## 🧹 Data Cleaning Pipeline (Power Query)

The automated M script ([`PowerQuery_Transformations.m`](./PowerQuery_Transformations.m)) cleans the raw dataset:
1. **Deduplication**: Audited and eliminated 15 duplicate transaction rows based on `Row ID`.
2. **Text Standardization**: Trimmed leading/trailing whitespace on `Customer Name` and converted `Segment` and `Ship Mode` to Proper Case (`Text.Proper`).
3. **Missing Value Imputation**: Resolved 50 missing postal code values via city mapping fallbacks.
4. **Strict Schema Typecasting**: Enforced `Currency.Type` for monetary fields, `Int64.Type` for quantities, and `type date` for timestamps.
5. **Enrichment Columns**: Calculated operational turnaround `[Shipping Days]` and line-level profitability `[Line Margin %]`.

---

## 📊 DAX Measures Calculation Engine

All measures are centralized inside a dedicated **`_Measures`** table and classified into logical display folders:

| Folder | Measure Name | DAX Expression | Verified Benchmark |
| :--- | :--- | :--- | :--- |
| **01 Core** | **Total Sales** | `SUM(Fact_Orders[Sales])` | **$4,485,117.51** |
| **01 Core** | **Total Profit** | `SUM(Fact_Orders[Profit])` | **$1,423,287.51** |
| **01 Core** | **Total Orders** | `DISTINCTCOUNT(Fact_Orders[Order ID])` | **2,501 Orders** |
| **01 Core** | **Total Quantity** | `SUM(Fact_Orders[Quantity])` | **19,979 Units** |
| **02 Ratios** | **Average Order Value** | `DIVIDE([Total Sales], [Total Orders], 0)` | **$1,793.33** |
| **02 Ratios** | **Profit Margin %** | `DIVIDE([Total Profit], [Total Sales], 0)` | **31.73%** |
| **03 Time Int.** | **Previous Year Sales** | `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Calendar[Date]))` | **$1,395,100.33 (2024)** |
| **03 Time Int.** | **Sales Growth %** | `DIVIDE([Total Sales] - [Previous Year Sales], [Previous Year Sales], BLANK())` | **+11.56% (2024)** |
| **03 Time Int.** | **Year-to-Date Sales** | `TOTALYTD([Total Sales], Dim_Calendar[Date])` | Dynamic Cumulative |
| **04 Dynamic** | **Top 10 Products Sales**| `CALCULATE([Total Sales], KEEPFILTERS(TOPN(10, ALLSELECTED(Dim_Products[Product Name]), [Total Sales], DESC)))` | Dynamic Top 10 |

---

## 🖥 Interactive Dashboard Suite (5 Pages)

The dashboard is built on a 16:9 widescreen canvas styled using a custom executive theme ([`SalesVision_Theme.json`](./SalesVision_Theme.json)):

### 1. Executive Overview
- High-impact KPI scorecard displaying Total Sales, Profit, Margin %, Orders, and AOV.
- 12-month revenue trajectory vs. prior year performance.
- Departmental sales & profit distribution (Technology, Furniture, Office Supplies).
- Regional revenue share donut and customer segment breakdown.

### 2. Sales Trends & Time Intelligence
- Monthly actual revenue vs. prior year comparison.
- Cumulative YTD sales tracking curve.
- Revenue breakdown by Day of Week and Weekend vs. Weekday demand.

### 3. Product Performance & Profitability
- Top 10 revenue-generating SKUs ranking.
- Sub-category quadrant scatter analysis (Sales Volume vs. Profit Margin %).
- Expandable hierarchical matrix with red/yellow/green margin conditional formatting.

### 4. Regional Performance & Territory Mapping
- Interactive geospatial bubble map across 19 major metropolitan hubs.
- State-level revenue rankings.
- Fulfillment lead-time efficiency matrix comparing shipping modes across regions.

### 5. Customer Analysis & Segment Economics
- Volume and profit contribution by segment (Consumer, Corporate, Home Office).
- Top 10 high-value customers.
- Annual purchasing frequency and Average Order Value evolution.

---

## ⚡ Advanced Power BI Features
- **Cross-Page Synchronized Slicers**: Slicing by Year or Region propagates across all 5 report tabs with a one-click **"Reset Filters"** action button.
- **Diagnostic Drill-Through Page**: Right-clicking any product bar instantly navigates to `Product_Drillthrough`, revealing item-level trends, margin breakdowns, and order logs.
- **Custom Report Page Tooltips**: Hovering over any category bar pops up an inline mini sparkline trendline (`Tooltip_CategoryTrend`) without cluttering the screen.
- **Context-Aware Dynamic Titles**: DAX-generated headers that adapt to active filters in real-time.
- **HEX-Driven Conditional Formatting**: Color codes managed dynamically via DAX measures (`#10B981` Emerald for positive growth, `#EF4444` Red for decline).
- **Bookmark View Switcher**: One-click toggle allowing executives to switch between high-level **Chart View** and detailed **Table View**.

---

## 💡 Key Business Insights & Strategic ROI

1. **The 50% Discount Trap (Direct -$37.8K Leak)**:
   - At 0% discount, the enterprise achieves a **43.56% profit margin**.
   - At 50% discount, the company operates at a net loss of **-13.20% (-$37,830.11 across 773 orders)**.
   - *Recommendation:* Restrict maximum sales representative discount authorization to **25%** to immediately reclaim **$55,000+** in lost annual profit.
2. **Catalog Margin Divergence (Laptops vs. Phones)**:
   - Laptops generate 29% of company revenue ($1.32M) but operate at low margins (~17.8%–18.0%) due to high procurement costs.
   - Flagship smartphones and solid oak conference tables maintain **>30.5% margins**.
   - *Recommendation:* Implement mandatory cross-selling bundles linking laptops with high-margin accessories (Webcams, Keyboards, Headsets at 40%+ margins).
3. **East Coast Market Expansion Opportunity**:
   - The South leads sales at **$1.22M (32.07% margin)**.
   - The East generates only **$886K (19.77% share)** despite high margins (31.63%).
   - *Recommendation:* Allocate 15% more marketing budget to high-density metros in New York, Boston, and Philadelphia to capture untapped market share.

---

## 🚀 Project Setup & Local Replication

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nilesh39/-Sales-Vision.git
   cd -Sales-Vision
   ```
2. **Data Pipeline**:
   - Raw source file: `SalesVision_Raw_Data.csv`
   - Cleaned analytical source: `SalesVision_Cleaned_Data.csv`
   - Normalized Star Schema tables: `Fact_Orders.csv`, `Dim_Customers.csv`, `Dim_Products.csv`, `Dim_Geography.csv`
3. **Open in Power BI Desktop**:
   - Launch Power BI Desktop $\rightarrow$ Click **Get Data** $\rightarrow$ Load the normalized CSV files.
   - Apply the custom theme via **View $\rightarrow$ Themes $\rightarrow$ Browse for themes $\rightarrow$ `SalesVision_Theme.json`**.
   - Create `Dim_Calendar` using the provided [`Dim_Calendar.dax`](./Dim_Calendar.dax) script.
   - Create the `_Measures` table and copy measures from [`DAX_Measures_Library.dax`](./DAX_Measures_Library.dax).

---

## 👨‍💻 Author & Resume Profile

**Nilesh**  
*Aspiring Business Intelligence Analyst & Power BI Developer | Bachelor of Computer Applications (BCA)*  
- **GitHub**: [github.com/Nilesh39](https://github.com/Nilesh39)
- **Repository**: [github.com/Nilesh39/-Sales-Vision](https://github.com/Nilesh39/-Sales-Vision.git)

---
*Developed with enterprise best practices following Kimball Dimensional Modeling, Power Query M Transformations, and Advanced DAX Time Intelligence.*
