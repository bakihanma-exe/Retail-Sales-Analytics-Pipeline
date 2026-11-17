# Source data

Place permitted retail CSV extracts in this folder under `raw/`. Expected logical files:

- Product.csv
- Region.csv
- Reseller.csv
- Sales.csv
- Salesperson.csv
- SalespersonRegion.csv
- Target.csv

The exact filenames, column names, data types, and primary keys must be confirmed against the dataset you use. Do not assume the sample column names in SQL/notebooks match every retail dataset.

Raw data is intentionally excluded from Git using `.gitignore`. Do not commit confidential, personal, or licensed data unless redistribution is allowed.
