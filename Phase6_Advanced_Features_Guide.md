# SalesVision – Advanced Power BI Features Implementation Manual
## Phase 6: Enterprise Interactivity, Navigation, Tooltips & Dynamic UX

This manual walks through the implementation of the 7 advanced capabilities that elevate SalesVision from a basic reporting dashboard into an interactive enterprise business intelligence tool.

---

### Feature 1: Synchronized Slicers & Global Reset Button
- **Sync Slicers**:
  1. In Power BI Desktop: Click the `Dim_Calendar[Year]` slicer on Page 1.
  2. Go to the top ribbon $\rightarrow$ Click **View** $\rightarrow$ Check **Sync slicers** pane.
  3. In the Sync Slicers pane on the right: Check the boxes for **Sync** (icon with refresh arrows) and **Visible** (eye icon) across all 5 report pages. Now, selecting "2024" on Page 1 automatically filters Pages 2, 3, 4, and 5!
- **Clear All Slicers (Reset) Button**:
  1. Go to **Insert** ribbon $\rightarrow$ **Buttons** $\rightarrow$ **Clear all slicers**.
  2. Place it in the top-right header area.
  3. In Format Button: Set text to "Reset Filters", add a subtle border, and set Icon color to `#64748B`.
  4. Action is automatically set to "Clear all slicers".

---

### Feature 2: Hierarchical Drill-Down & Drill-Through Engine

#### A. Drill-Down on Charts:
1. In Page 3 (Product Performance), select the Category Bar Chart.
2. In the **Y-Axis** field well, drag in:
   - Level 1: `Dim_Products[Category]`
   - Level 2: `Dim_Products[Sub-Category]`
   - Level 3: `Dim_Products[Product Name]`
3. When hovering over the visual, Power BI reveals the Drill-Down header icons:
   - **Double down-arrow (`↓↓`)**: Drills to the next hierarchy level for the entire dataset.
   - **Forked arrow (`↓-↓`)**: Expands the hierarchy.
   - **Single down-arrow (`↓`)**: Turns on selective drill-down (clicking "Technology" drills directly into Phones, Laptops, Accessories!).

#### B. Dedicated Drill-Through Page (`Product Details Drillthrough`):
1. Create a new page named **`Product_Drillthrough`**.
2. In the **Visualizations** pane under **Page Information / Drill-through**:
   - Set "Allow use as": **Drill-through**.
   - Drag `Dim_Products[Product Name]` and `Dim_Products[Category]` into the **Drill-through fields** well.
   - Ensure "Keep all filters" is toggled **On**.
3. Power BI will automatically create a back button (`←`) in the top left.
4. On this page, build:
   - A Dynamic Card Header: `_Measures[Drillthrough Product Header]`.
   - KPI Cards: Units Sold, Total Sales, Total Profit, Profit Margin %.
   - Monthly Sales Trendline for this specific product.
   - Customer Table: List of all customers who purchased this SKU with dates, quantities, and order IDs.
5. **How to test**: Go to Page 1 or Page 3 $\rightarrow$ Right-click any product (e.g. `ProBook Elite 15.6 Laptop`) $\rightarrow$ Click **Drill-through** $\rightarrow$ Select **Product_Drillthrough**. The page instantly loads the diagnostic view for that exact item!

---

### Feature 3: Modern Report Page Tooltips (Custom Sparkline Popups)
1. Create a new page and name it **`Tooltip_CategoryTrend`**.
2. In the **Format Page** pane $\rightarrow$ **Page Information**:
   - Toggle **Allow use as tooltip** to **On**.
3. Under **Canvas Settings**:
   - Type: **Custom**
   - Width: **320 px**
   - Height: **220 px**
4. On this canvas, add:
   - A Card visual showing `_Measures[Total Profit]` and `_Measures[Profit Margin %]`.
   - A mini Area Chart showing `Dim_Calendar[Month Short]` (X-axis) vs `_Measures[Total Sales]` (Y-axis).
5. **Attach to Visuals**:
   - Go back to Page 1 (Executive Overview) $\rightarrow$ Select the **Category Bar Chart**.
   - In **Format visual** pane $\rightarrow$ **General** $\rightarrow$ **Tooltips**:
     - Type: **Report page**
     - Page: **`Tooltip_CategoryTrend`**.
   - Hover over "Technology" or "Furniture"—the mini trendline chart instantly pops up inline!

---

### Feature 4: Dynamic DAX-Driven Chart Titles
1. Select the Category Revenue chart on Page 1.
2. In **Format visual** $\rightarrow$ **General** $\rightarrow$ **Title**.
3. Next to the "Text" input box, click the **Conditional Formatting button (`fx`)**.
4. In the dialog:
   - *Format style:* **Field value**
   - *What field should this be based on?* $\rightarrow$ Select **`_Measures[Dynamic Category Title]`**.
   - Click **OK**.
5. The title now automatically adapts: e.g., *"Revenue & Margin Breakdown | Category: Technology | Region: West (2024)"*.

---

### Feature 5: Advanced Conditional Formatting (Data Bars & KPI Colors)
1. **Sales Growth KPI Card**:
   - Select the Sales Growth Card on Page 2.
   - In **Format visual** $\rightarrow$ **Callout value** $\rightarrow$ Click **`fx`** next to Color.
   - *Format style:* **Field value** $\rightarrow$ Select **`_Measures[Sales Growth Color KPI]`**.
   - Result: If growth is positive, the number displays in Emerald Green (`#10B981`); if negative, it automatically turns Coral Red (`#EF4444`).
2. **Matrix Table Margins**:
   - In Page 3's Product Matrix table, select the `Profit Margin %` field.
   - Right-click or expand the field dropdown in the Values well $\rightarrow$ **Conditional formatting** $\rightarrow$ **Background color**.
   - Format style: **Field value** $\rightarrow$ Select **`_Measures[Profit Margin Background Color]`**.
   - For text color, select **`_Measures[Profit Margin Text Color]`**.
   - Result: High margins highlight in soft green, acceptable in soft blue, and margin-eroding products highlight in warning red.

---

### Feature 6: Bookmarks & View Toggle (Switch Between "Chart View" & "Table View")
1. On Page 3 (Product Performance), place the **Top 10 Bar Chart** and the **Product Matrix Table** in the exact same screen location.
2. Open the **Selection** pane and the **Bookmarks** pane (under View ribbon).
3. **Bookmark 1: "Show Chart"**:
   - In Selection pane, hide the Table (click the eye icon so it is invisible) and show the Bar Chart.
   - In Bookmarks pane, click **Add** $\rightarrow$ Rename to **`View_Chart`**.
   - Uncheck "Data" (so filtering doesn't reset when toggling) and keep "Display" checked.
4. **Bookmark 2: "Show Table"**:
   - In Selection pane, hide the Bar Chart and show the Table.
   - In Bookmarks pane, click **Add** $\rightarrow$ Rename to **`View_Table`**.
   - Uncheck "Data" and keep "Display" checked.
5. **Add Toggle Buttons**:
   - Insert two buttons or a Bookmark Navigator: "Chart View" and "Table View".
   - Assign Action $\rightarrow$ Type: **Bookmark** $\rightarrow$ Select `View_Chart` and `View_Table` respectively.
   - The user can now seamlessly toggle between graphical and tabular views with 1 click!

---

### Feature 7: Executive Navigation Bar (Page Navigator)
1. Go to **Insert** ribbon $\rightarrow$ **Buttons** $\rightarrow$ **Navigator** $\rightarrow$ **Page navigator**.
2. Place the navigation bar in a clean left vertical strip (Width: 160px) or along the top header.
3. In **Format Navigator**:
   - Under *Pages*, hide the Tooltip and Drill-through pages so only the 5 main pages show.
   - Shape: Rounded rectangle (4px).
   - Style: Default state (Soft Grey font), Selected state (Cobalt Blue `#2563EB` fill with White text).
4. Gives the report the sleek look and feel of a custom SaaS web application!
