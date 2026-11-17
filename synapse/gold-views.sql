-- Synapse Serverless SQL template inspired by the supplied walkthrough.
-- Configure the external data source / credential for your ADLS Gen2 account first.
-- Replace <storage-account>, <container>, paths, and schema to match your environment.

-- Example: query Silver Parquet directly with OPENROWSET.
-- CREATE OR ALTER VIEW gold.vw_sales_by_territory AS
-- SELECT
--     TerritoryKey,
--     SUM(CAST(OrderQuantity AS bigint)) AS TotalOrderQuantity
-- FROM OPENROWSET(
--     BULK 'https://<storage-account>.dfs.core.windows.net/<container>/silver/sales/*.parquet',
--     FORMAT = 'PARQUET'
-- ) AS rows
-- GROUP BY TerritoryKey;

-- The source document describes creating a Gold schema and views over Silver data.
-- Keep actual column names and file paths aligned with the Parquet output.
