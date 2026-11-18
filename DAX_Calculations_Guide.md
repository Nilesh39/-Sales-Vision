# SalesVision – DAX Measures & Technical Deep-Dive
## Phase 4: Business Intelligence Calculation Engine

### 1. Executive Summary & Verified Benchmarks
All calculations have been pre-computed and cross-validated against [`Fact_Orders.csv`](file:///d:/PowerBI_1/Fact_Orders.csv) and [`Dim_Products.csv`](file:///d:/PowerBI_1/Dim_Products.csv).

| Metric | Power BI Measure Name | Verified Expected Benchmark | Format String |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | `[Total Sales]` | **$4,485,117.51** | `$#,##0.00` |
| **Total Profit** | `[Total Profit]` | **$1,423,287.51** | `$#,##0.00` |
| **Total Orders** | `[Total Orders]` | **2,501** | `#,##0` |
| **Total Units** | `[Total Quantity]` | **19,979** | `#,##0` |
| **Average Order Value**| `[Average Order Value]`| **$1,793.33** | `$#,##0.00` |
| **Overall Profit Margin**| `[Profit Margin %]` | **31.73%** | `0.00%` |
| **2023 Sales** | `[Total Sales]` (Filtered to 2023) | **$1,395,100.33** | `$#,##0.00` |
| **2024 Sales** | `[Total Sales]` (Filtered to 2024) | **$1,556,386.53** | `$#,##0.00` |
| **2024 YoY Growth** | `[Sales Growth %]` (In 2024) | **+11.56%** | `0.00%` |
| **2025 Sales** | `[Total Sales]` (Filtered to 2025) | **$1,533,630.65** | `$#,##0.00` |
| **2025 YoY Growth** | `[Sales Growth %]` (In 2025) | **-1.46%** | `0.00%` |
| **Avg Shipping Days** | `[Average Shipping Turnaround Days]`| **3.43 Days** | `0.0` |

---

### 2. Deep-Dive: Explanation of Core DAX Concepts

#### A. Filter Context vs. Row Context
- **Row Context**: Evaluates row-by-row inside an iterator (like `SUMX` or a calculated column).
- **Filter Context**: The active slice of data created by visuals, rows/columns of a matrix, and slicers on the report page. Measures compute strictly within the current filter context.

#### B. The Superpower of `CALCULATE()`
- `CALCULATE` is the single most important function in DAX. It is the **only** function that can modify, override, or expand the current Filter Context.
- In `[Previous Year Sales]`, `CALCULATE` takes the current date selection and instructs Power BI to replace it with dates shifted back by 1 year using `SAMEPERIODLASTYEAR()`.

#### C. Safe Division with `DIVIDE()`
- Traditional `/` operator causes division-by-zero errors (`#DIV/0!`, `Infinity`, or `NaN`) if a denominator has 0 sales or orders.
- `DIVIDE([Total Sales], [Total Orders], 0)` safely intercepts zero-denominator cases and returns a clean alternative value (or `BLANK()`).

#### D. Variables (`VAR ... RETURN`)
- Using variables in `[Sales Growth %]` caches intermediate results in memory so they are calculated only once rather than re-computed twice, boosting query speed by up to 40%.
- Makes formulas readable and easy to debug.
