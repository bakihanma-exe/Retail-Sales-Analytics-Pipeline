# Power BI dashboard design

## Page 1 — Executive overview
- Total sales
- Sales target and target attainment %
- Sales versus previous period
- Monthly sales trend
- Sales by region

## Page 2 — Product performance
- Sales by category and subcategory
- Top 5 products per category
- Product contribution to total sales

## Page 3 — Sales team and reseller performance
- Sales by salesperson
- Sales by reseller
- Region / salesperson drill-down

## Suggested model
Use a fact table at a clearly documented sales transaction grain, with dimensions such as Date, Product, Region, Reseller, and Salesperson. Confirm keys and relationship cardinalities from the actual source data before building relationships.

## KPI definitions to confirm
- Total Sales: sum of the agreed sales amount column.
- Target Attainment %: actual sales divided by target, with zero / missing targets handled explicitly.
- Average Order Value: total sales divided by distinct order count, if an order identifier exists.

Use Gold tables as the reporting source. Validate all KPI definitions with the business before publishing.
