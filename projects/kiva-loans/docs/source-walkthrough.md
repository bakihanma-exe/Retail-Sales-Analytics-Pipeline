# Kiva source walkthrough — extracted from the supplied PDF

## Business context (pages 4–5)
The walkthrough uses the Kaggle competition dataset “Data Science for Good: Kiva Crowdfunding”. It describes loans issued between January 2014 and July 2017 and assumes new data arrives daily. SQL Server is the source database.

## Architecture / security (pages 5–7)
- On-prem SQL Server is the source.
- ADF connects through Self-Hosted Integration Runtime.
- ADLS Gen2 has Bronze, Silver and Gold containers.
- Databricks performs two transformation levels.
- Synapse Serverless SQL exposes Gold data.
- Power BI consumes Synapse views.
- SQL Server username/password are stored in Azure Key Vault; ADF managed identity is granted secret access.
- The walkthrough describes a SQL login with db_datareader access to dbo tables.

**Security warning:** Do not reproduce the sample login/password text or any real secrets from the PDF. Treat any exposed credential as compromised and rotate it.

## Ingestion (pages 8–10)
- Create Lookup query to enumerate tables under dbo.
- ForEach iterates over Lookup output.
- Copy Activity dynamically reads each table and writes it to a separate Bronze folder as CSV.
- Debug and trigger are used to test.
- The walkthrough says each successful run overwrites the existing Bronze folder.

## Databricks transformations (pages 11–16)
- The walkthrough mounts Bronze, Silver and Gold containers.
- Bronze-to-Silver iterates through table folders and changes columns whose names contain “date” or “time” to a date-formatted string.
- Silver-to-Gold iterates through tables and lowercases column names.
- ADF calls the two Databricks notebooks sequentially after ingestion.

## Synapse serving (pages 17–18)
- Create a Serverless SQL database named gold_db.
- A stored procedure creates a view for each Gold folder using OPENROWSET with CSV format.
- ADF Get Metadata reads Gold table folders; ForEach invokes the stored procedure.

## Power BI (pages 19–23)
- Connect to Synapse Serverless SQL endpoint and import views.
- Apply Power Query data types; create a separate date table; relate it to kiva_loans.
- Dashboard visuals: total loan count, total loan amount, funded amount, sector share, borrower gender distribution, repayment interval by gender, country ranking, and monthly loan versus funded trend.
- PDF dashboard values: ~671K loans, $565.4M total loan amount, $527.6M funded amount.
- Pipeline test: add 10 random rows, trigger the pipeline, refresh Power BI; repeat daily for five days.

## Gaps / caveats identified
1. The ingestion is described as overwrite/full refresh; the testing narrative mentions adding rows but does not show a watermark or CDC design.
2. Date/time conversion uses string formatting and may lose timestamp semantics; confirm source types and choose DateType/TimestampType intentionally.
3. Lowercasing column names alone is not a complete Gold business transformation.
4. The stored procedure concatenates a view name into dynamic SQL; validate identifiers and quote safely.
5. OPENROWSET schema inference and CSV parsing need explicit testing, especially headers and data types.
6. The document does not provide the actual source SQL schema, table inventory, or full data files.
7. The PDF dashboard values should be recomputed from the exact dataset and filters.
8. The PDF uses legacy DBFS mount / credential passthrough examples; use supported secure access for a current deployment.
