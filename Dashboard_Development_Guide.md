# SalesVision – Dashboard Development Guide & Visual Layout
## Phase 5: Multi-Page Executive BI Report Implementation

### 1. Global Report Canvas & Theme Setup
- **Canvas Size**: 16:9 Standard Widescreen (`1280 x 720` pixels).
- **Import Custom Theme**:
  - In Power BI Desktop: Go to **View** ribbon $\rightarrow$ Click the dropdown arrow on **Themes** $\rightarrow$ Click **Browse for themes** $\rightarrow$ Select [`SalesVision_Theme.json`](file:///d:/PowerBI_1/SalesVision_Theme.json).
  - This automatically configures executive fonts (Segoe UI), colors (Cobalt Blue `#2563EB`, Emerald `#10B981`, Slate Navy `#0F172A`), rounded container borders (8px radius), and clean white card backgrounds.

---

### 2. Multi-Page Architecture Overview

The SalesVision suite comprises 5 specialized analytical pages:
1. **Executive Overview**: High-level corporate health scorecard and revenue velocity.
2. **Sales Trends**: Longitudinal performance, YoY variances, and seasonal patterns.
3. **Product Performance**: SKU-level profit margins, catalog volume, and sub-category matrix.
4. **Regional Performance**: Geospatial territory analysis, city/state profitability, and shipping turnaround.
5. **Customer Analysis**: Segment purchasing power, customer lifetime spend, and order frequency.

---

### 3. Detailed Page-by-Page Visual Specification

#### PAGE 1: Executive Overview
* **Header Banner (Top, Height: 70px)**:
  - Text: **SalesVision | Executive Performance Dashboard**
  - Subtitle: `[Sales KPI Card Subtitle]` (Dynamic measure displaying date range).
  - Global Slicers: `Dim_Calendar[Year]` (Tile / Pill buttons), `Dim_Geography[Region]` (Dropdown).

* **Row 1: Executive KPI Cards (Y: 85px, Height: 95px)**:
  - **Card 1: Total Sales** $\rightarrow$ Field: `_Measures[Total Sales]` (Callout: 24pt Bold, Data Label: Currency `$#,##0.00`).
  - **Card 2: Total Profit** $\rightarrow$ Field: `_Measures[Total Profit]` (Callout: 24pt Bold).
  - **Card 3: Profit Margin %** $\rightarrow$ Field: `_Measures[Profit Margin %]` (Callout: 24pt Bold).
  - **Card 4: Total Orders** $\rightarrow$ Field: `_Measures[Total Orders]` (Callout: 24pt Bold).
  - **Card 5: Average Order Value (AOV)** $\rightarrow$ Field: `_Measures[Average Order Value]` (Callout: 24pt Bold).

* **Row 2: Trend & Category Breakdown (Y: 195px, Height: 245px)**:
  - **Visual 1: Monthly Sales Trend (Area / Line Chart)**
    - X-Axis: `Dim_Calendar[Month Short]`
    - Y-Axis: `_Measures[Total Sales]`
    - Secondary Y-Axis / Comparison Line: `_Measures[Previous Year Sales]`
    - Title: "Monthly Revenue Trajectory vs. Previous Year"
  - **Visual 2: Sales & Profit by Category (Clustered Bar Chart)**
    - Y-Axis: `Dim_Products[Category]`
    - X-Axis: `_Measures[Total Sales]`, `_Measures[Total Profit]`
    - Data Labels: Enabled.

* **Row 3: Geography & Segment Share (Y: 455px, Height: 245px)**:
  - **Visual 3: Regional Sales Contribution (Donut Chart)**
    - Legend: `Dim_Geography[Region]`
    - Values: `_Measures[Total Sales]`
    - Detail Labels: "Category, percent of total"
  - **Visual 4: Sales by Customer Segment (100% Stacked Bar or Donut)**
    - Legend: `Dim_Customers[Segment]`
    - Values: `_Measures[Total Sales]`
    - Title: "Revenue Split by Customer Segment"

---

#### PAGE 2: Sales Trends & Time Intelligence
* **Top KPI Row**:
  - `_Measures[Year-to-Date Sales]`
  - `_Measures[Prior Year YTD Sales]`
  - `_Measures[Sales Growth %]` (with green/red conditional callout)
  - `_Measures[YoY Sales Variance]`

* **Visual 1: Monthly Revenue vs. Prior Year (Line and Clustered Column Chart)**:
  - X-Axis: `Dim_Calendar[Month Short]`
  - Column Y-Axis: `_Measures[Total Sales]`
  - Line Y-Axis: `_Measures[Previous Year Sales]`
  - Data Labels: On for columns.

* **Visual 2: Cumulative YTD Sales Curve (Line Chart)**:
  - X-Axis: `Dim_Calendar[Month Short]`
  - Y-Axis: `_Measures[Year-to-Date Sales]`, `_Measures[Prior Year YTD Sales]`
  - Purpose: Shows exactly when the current year outpaced or lagged the previous year.

* **Visual 3: Sales by Day of Week (Column Chart)**:
  - X-Axis: `Dim_Calendar[Day of Week Short]` (Sorted by `Day of Week Number`)
  - Y-Axis: `_Measures[Total Sales]`
  - Legend: `Dim_Calendar[Is Weekend]`

---

#### PAGE 3: Product Performance & Profitability
* **Visual 1: Top 10 Revenue Generating Products (Horizontal Bar Chart)**:
  - Y-Axis: `Dim_Products[Product Name]` (Filter: Top N $\rightarrow$ Top 10 by `[Total Sales]`)
  - X-Axis: `_Measures[Total Sales]`
  - Data Labels: Value inside end.

* **Visual 2: Profit Margin vs. Sales by Sub-Category (Scatter Plot / Quadrant Analysis)**:
  - X-Axis: `_Measures[Total Sales]`
  - Y-Axis: `_Measures[Profit Margin %]`
  - Values: `Dim_Products[Sub-Category]`
  - Size: `_Measures[Total Quantity]`
  - Reference Lines: Add average profit margin line (31.7%) across the Y-axis. Sub-categories below the line are margin-diluting!

* **Visual 3: Comprehensive Product Catalog Matrix (Table/Matrix)**:
  - Rows: `Dim_Products[Category]`, `Dim_Products[Sub-Category]`, `Dim_Products[Product Name]`
  - Values: `[Total Quantity]`, `[Total Sales]`, `[Total Profit]`, `[Profit Margin %]`
  - Conditional Formatting: Background color gradient on `[Profit Margin %]` (Red $\rightarrow$ Yellow $\rightarrow$ Green).

---

#### PAGE 4: Regional Performance & Logistics
* **Visual 1: Geographic Territory Bubble Map (Map Visual)**:
  - Location: `Dim_Geography[State]`, `Dim_Geography[Country]`
  - Bubble Size: `_Measures[Total Sales]`
  - Color saturation / Tooltip: `_Measures[Total Profit]`

* **Visual 2: Revenue & Margin by State (Bar Chart)**:
  - Y-Axis: `Dim_Geography[State]`
  - X-Axis: `_Measures[Total Sales]`
  - Color / Tooltips: `_Measures[Profit Margin %]`

* **Visual 3: Logistics & Fulfillment Efficiency (Matrix)**:
  - Rows: `Dim_Geography[Region]`
  - Values: `[Total Sales]`, `[Total Orders]`, `[Average Shipping Turnaround Days]`, `[Profit Margin %]`
  - Highlights shipping bottlenecks across territories.

---

#### PAGE 5: Customer Intelligence & Segmentation
* **Visual 1: Segment Contribution Breakdown (Donut Chart)**:
  - Legend: `Dim_Customers[Segment]`
  - Values: `_Measures[Total Sales]`
  - Tooltips: `[Total Profit]`, `[Total Orders]`, `[Average Order Value]`

* **Visual 2: Top 10 Customers by Revenue (Bar Chart)**:
  - Y-Axis: `Dim_Customers[Customer Name]` (Filtered Top 10 by `[Total Sales]`)
  - X-Axis: `_Measures[Total Sales]`
  - Tooltips: `[Total Orders]`, `[Profit Margin %]`

* **Visual 3: Customer Purchase Frequency & AOV Matrix**:
  - Rows: `Dim_Customers[Segment]`
  - Columns: `Dim_Calendar[Year]`
  - Values: `[Average Order Value]`, `[Total Orders]`
