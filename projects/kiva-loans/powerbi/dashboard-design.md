# Kiva Power BI dashboard design

The source walkthrough describes the following report elements.

## KPI cards
- Total loans: distinct/count of loan identifier (confirm source key).
- Total loan amount: sum of loan amount.
- Total funded amount: sum of funded amount.

## Visuals
- Bar chart: percentage of loans by sector.
- Doughnut chart: borrower gender groups (Male, Female, Other/Group).
- Clustered column chart: repayment interval by borrower gender.
- Table: loan distribution by country, descending.
- Line chart: monthly total loan amount versus funded amount.
- Slicers: Year and Month.

## Model
Create a dedicated Date table and relate it to the Kiva loan date column. Confirm relationship cardinality and date data types. The source walkthrough reports importing Synapse views into Power BI and using Power Query to correct types.

## Reference values in the PDF
Approximately 671K loans, $565.4M total loan amount, and $527.6M funded amount. Recompute from the actual source and report filters before using these as validated KPIs.
