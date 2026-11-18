# SalesVision – Resume Bullet Points & Technical Interview Preparation
## Professional Portfolio Dossier for Nilesh (BCA Graduate)

---

### 1. High-Impact Resume Project Bullet Points

Use these tailored bullet points in your **Projects** or **Experience** section on your resume:

#### Option A: Comprehensive Multi-Bullet Format (Recommended for Resume)
**SalesVision – Enterprise Sales Performance & BI Platform | Power BI, DAX, Power Query, Python**
- Engineered an end-to-end Power BI business intelligence dashboard analyzing **$4.49M in gross revenue** across **7,500 transactions** (2023–2025) to empower executive leadership with data-driven decision-making.
- Designed an automated **Power Query (M) ETL pipeline** to clean, deduplicate, and typecast raw transactional records, achieving 100% data integrity and eliminating 15 duplicate order rows.
- Architected an optimized **Kimball Star Schema** comprising 1 central Fact table (`Fact_Orders`) and 4 Dimension tables (`Dim_Customers`, `Dim_Products`, `Dim_Geography`, `Dim_Calendar`), enforcing 1-to-Many single-directional filtering.
- Authored **16+ production DAX measures** utilizing `CALCULATE`, `SAMEPERIODLASTYEAR`, `TOTALYTD`, `DIVIDE`, and `TOPN` to calculate Time Intelligence KPIs, YoY sales growth (+11.56% in 2024), and Average Order Value ($1,793.33).
- Built advanced UX features including **cross-page synchronized slicers**, **hierarchical drill-down**, a dedicated **product diagnostic drill-through page**, custom **sparkline report tooltips**, and dynamic DAX-driven titles.
- Identified a critical **-$37.8K margin leak** caused by unconstrained 50% promotional discounting, providing strategic recommendations to cap discounting at 25% and reclaim **$55,000+ in annual operating profit**.

#### Option B: Compact 3-Bullet Format (For Single-Page Resumes)
- Developed **SalesVision**, a 5-page enterprise Power BI dashboard analyzing $4.49M in multi-year retail transactions across 4 geographic regions.
- Modeled a high-performance **Star Schema** with a custom DAX Date Dimension and 16 advanced DAX measures for YoY time intelligence, ranking, and customer segmentation.
- Uncovered a key profitability bottleneck where 50% discounting generated a -13.2% net loss; presented data-driven recommendations to leadership to reclaim $55K+ in margin.

---

### 2. Portfolio & LinkedIn Summary Write-Up

> **Headline:** Power BI Project Showcase: SalesVision – Sales Performance & BI Dashboard  
> **Summary:**  
> Excited to showcase my latest end-to-end Business Intelligence project: **SalesVision**! 🚀  
> 
> As part of this project, I acted as the Lead BI Developer to solve a realistic business challenge: executive management needed visibility into multi-year sales velocity, regional profitability, and discounting leaks.
> 
> **Key Technical Highlights:**
> 🔹 **Data Ingestion & ETL:** Automated data cleansing using Power Query (M Language) to handle duplicates, whitespace, and typecasting.  
> 🔹 **Data Modeling:** Implemented a pure Kimball Star Schema with Fact and Dimension tables, eliminating bidirectional filters to optimize VertiPaq engine caching.  
> 🔹 **Advanced DAX:** Built custom Time Intelligence calculations (YoY Growth, YTD, PY Sales, AOV, Profit Margin %).  
> 🔹 **Interactive UX:** Designed custom report page tooltips (mini sparklines), product drill-through pages, synchronized slicers, and bookmark view toggles.  
> 🔹 **Strategic Impact:** Discovered that orders discounted at 50% caused an outright net loss of -$37.8K, and formulated actionable pricing governance policies.  
> 
> Check out the complete open-source repository, documentation, and DAX library on GitHub: https://github.com/Nilesh39/-Sales-Vision.git

---

### 3. Top 10 Technical Interview Questions & Senior Answers

#### Q1: "Can you walk me through the architecture of your SalesVision project?"
**Answer:**  
*"SalesVision is an end-to-end BI solution built using Kimball Dimensional Modeling. I started with a raw transactional extract of 7,515 rows. In Power Query, I built an automated M pipeline that deduplicated records, normalized casing, imputed missing postal codes, and enforced strict data types.  
I then normalized the data into a Star Schema with `Fact_Orders` at the center connected via 1-to-many single-direction relationships to `Dim_Customers`, `Dim_Products`, `Dim_Geography`, and a custom DAX-generated `Dim_Calendar`. On top of this model, I authored a dedicated `_Measures` table with 16 DAX calculations for YoY growth and margins, and deployed a 5-page interactive dashboard with custom tooltips and drill-through."*

#### Q2: "Why did you build a custom DAX Date table instead of using Power BI's Auto Date/Time?"
**Answer:**  
*"Power BI's built-in Auto Date/Time feature creates an invisible, separate date table in the background for every single date column in your dataset. In enterprise models with multiple dates (like Order Date and Ship Date), this wastes significant RAM and bloats the `.pbix` file.  
By building an explicit DAX Date table with `CALENDAR()` and marking it as an official Date Table, I achieved complete control over fiscal years, sort-by columns (e.g., sorting Month Name by Month Number), and enabled standard Time Intelligence functions like `SAMEPERIODLASTYEAR` and `TOTALYTD` while keeping the model lean and fast."*

#### Q3: "What is the difference between Row Context and Filter Context in DAX?"
**Answer:**  
*"Row Context exists when a formula iterates row-by-row through a table. It knows the values of the current row, but it cannot see the rest of the table or respect report slicers. Calculated columns and iterator functions like `SUMX` create row context.  
Filter Context, on the other hand, is the active slice of data applied to a visual. It is created by page slicers, matrix row/column headers, and report filters. Measures always evaluate within the active Filter Context. `CALCULATE` is the unique function that can transition row context into filter context and modify existing filter contexts."*

#### Q4: "Why did you use `DIVIDE([Total Sales], [Total Orders], 0)` instead of `[Total Sales] / [Total Orders]`?"
**Answer:**  
*"In DAX, using the basic forward slash `/` operator throws an error, `#DIV/0!`, or returns `Infinity` whenever the denominator is zero or null. In contrast, the `DIVIDE()` function has built-in safe division logic. It tests the denominator and, if zero, returns an optional third argument (such as `0` or `BLANK()`). This guarantees that KPI cards and visual averages render gracefully without breaking visual rendering."*

#### Q5: "What is the difference between Star Schema and Snowflake Schema, and why did you choose Star Schema?"
**Answer:**  
*"In a Star Schema, dimension tables are completely denormalized—each dimension connects directly to the central fact table. In a Snowflake Schema, dimensions are further normalized into sub-tables (for example, splitting Products into Categories and Sub-Categories as separate tables).  
I chose a Star Schema because Power BI's internal in-memory VertiPaq engine is specifically designed and optimized for Star Schemas. Star Schemas require fewer relationship joins, resulting in significantly faster DAX query execution, simpler DAX formulas, and a much cleaner user experience."*

#### Q6: "Why did you avoid Bi-Directional Cross-Filtering in your relationships?"
**Answer:**  
*"While bi-directional filtering might seem convenient, in enterprise models it introduces severe risks:  
1. **Ambiguous Paths**: It can create circular relationship loops where Power BI cannot determine which table filters which.  
2. **Performance Degradation**: VertiPaq has to evaluate filters in both directions simultaneously, slowing down visuals on large tables.  
3. **Unexpected Calculation Side Effects**: Measures may return unexpected totals because filters propagate backward through fact tables. Keeping relationships strictly single-directional (Dimension $\rightarrow$ Fact) guarantees clean, predictable filter propagation."*

#### Q7: "How did you implement the Previous Year Sales and Sales Growth % measures?"
**Answer:**  
*"For `[Previous Year Sales]`, I used:  
`CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Calendar[Date]))`.  
`SAMEPERIODLASTYEAR` takes the dates in the current filter context and shifts them back exactly one full year.  
For `[Sales Growth %]`, I used variables (`VAR` and `RETURN`) to store `CurrentSales` and `PriorYearSales`, and then computed `DIVIDE(CurrentSales - PriorYearSales, PriorYearSales, BLANK())`. Using variables ensures each measure is computed only once in memory, boosting performance."*

#### Q8: "How does a Drill-Through page work in Power BI?"
**Answer:**  
*"A Drill-Through page allows a user to right-click a data point on a summary chart and navigate to a specialized target page filtered specifically for that selected entity.  
I created a `Product_Drillthrough` page and added `Dim_Products[Product Name]` into the Drill-through fields well with 'Keep all filters' enabled. Power BI automatically passes the product filter context to that page, rendering item-specific trends, margin breakdowns, and order logs, while providing a native back button to return."*

#### Q9: "What was the most significant business insight you discovered in SalesVision?"
**Answer:**  
*"The most eye-opening discovery was the '50% Discount Trap'. Management believed that high discounts were driving profitable volume. By analyzing profit margin across discount tiers, I proved that while 0% discounts yielded a healthy 43.6% margin, orders discounted at 50% resulted in an outright loss of **-13.2%**, draining **-$37.8K in net profit** across 773 orders. I recommended instituting an automated 25% discount cap in the CRM, which would immediately reclaim over $55,000 in annual profit."*

#### Q10: "How did you test and optimize dashboard performance?"
**Answer:**  
*"I followed a structured QA and optimization framework:  
1. **Referential Integrity Validation**: Ran automated scripts to confirm zero orphan foreign keys between Fact and Dimension tables.  
2. **Performance Analyzer**: Monitored visual rendering times, confirming DAX query execution times stayed well below 150 ms.  
3. **VertiPaq Memory Optimization**: Hid fact table foreign keys, removed unused technical columns like `Row ID`, and stored currencies as fixed decimal types to maximize run-length encoding (RLE) dictionary compression."*
