/*
========================================================================================
SalesVision - Power Query (M Code) Transformation Pipeline
Project: SalesVision - Sales Performance & Business Intelligence Dashboard
Author: Senior Power BI Developer & Business Intelligence Analyst
Purpose: Clean, standardize, typecast, and enrich raw sales transaction logs.
========================================================================================
Instructions:
1. In Power BI Desktop, go to "Home" -> "Transform Data" to open Power Query Editor.
2. In the "Home" tab, click "New Source" -> "Blank Query".
3. Click "Advanced Editor" in the Query tab.
4. Replace the entire code with the script below.
5. If your file path differs, update the FilePath parameter on line 17.
========================================================================================
*/

let
    // 1. Define File Path Source (Update this path to match your local file location)
    FilePath = "d:\PowerBI_1\SalesVision_Raw_Data.csv",
    
    // 2. Load the Raw CSV File
    RawSource = Csv.Document(
        File.Contents(FilePath),
        [Delimiter=",", Columns=23, Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    
    // 3. Promote the First Row as Column Headers
    PromotedHeaders = Table.PromoteHeaders(RawSource, [PromoteAllScalars=true]),
    
    // 4. Remove Duplicate Transaction Records
    // Eliminates redundant duplicate line items to prevent double-counting of revenue
    DeduplicatedData = Table.Distinct(PromotedHeaders, {"Row ID"}),
    
    // 5. Clean Text Inconsistencies & Whitespace
    // Trims leading/trailing whitespace from customer names
    TrimmedCustomerName = Table.TransformColumns(DeduplicatedData, {{"Customer Name", Text.Trim, type text}}),
    
    // Standardizes casing in Segment and Ship Mode to Proper Case (Capitalize Each Word)
    StandardizedCasing = Table.TransformColumns(
        TrimmedCustomerName,
        {
            {"Segment", Text.Proper, type text},
            {"Ship Mode", Text.Proper, type text}
        }
    ),
    
    // 6. Handle Missing / Blank Postal Codes
    // Replaces empty strings with standard "Unknown/Pending" or regional fallback
    HandledMissingPostal = Table.ReplaceValue(
        StandardizedCasing,
        "",
        "99999",
        Replacer.ReplaceValue,
        {"Postal Code"}
    ),
    
    // 7. Enforce Strict Data Types
    // Essential for high-performance VertiPaq compression in Power BI
    TypedData = Table.TransformColumnTypes(
        HandledMissingPostal,
        {
            {"Row ID", type text},
            {"Order ID", type text},
            {"Order Date", type date},
            {"Ship Date", type date},
            {"Ship Mode", type text},
            {"Customer ID", type text},
            {"Customer Name", type text},
            {"Segment", type text},
            {"Country", type text},
            {"City", type text},
            {"State", type text},
            {"Postal Code", type text},
            {"Region", type text},
            {"Product ID", type text},
            {"Category", type text},
            {"Sub-Category", type text},
            {"Product Name", type text},
            {"Unit Cost", Currency.Type},
            {"Unit Price", Currency.Type},
            {"Quantity", Int64.Type},
            {"Discount", Percentage.Type},
            {"Sales", Currency.Type},
            {"Profit", Currency.Type}
        }
    ),
    
    // 8. Add Calculated Column: Shipping Duration (Days)
    // Measures fulfillment turnaround time: [Ship Date] - [Order Date]
    AddedShippingDays = Table.AddColumn(
        TypedData, 
        "Shipping Days", 
        each Duration.Days([Ship Date] - [Order Date]), 
        Int64.Type
    ),
    
    // 9. Add Calculated Column: Line Margin %
    // Line-item level profitability ratio: Profit / Sales
    AddedLineMargin = Table.AddColumn(
        AddedShippingDays,
        "Line Margin %",
        each if [Sales] = 0 then 0.0 else ([Profit] / [Sales]),
        Percentage.Type
    )

in
    AddedLineMargin
