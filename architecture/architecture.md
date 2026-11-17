# Architecture and design

## End-to-end flow
1. AdventureWorks CSV files are hosted in a public GitHub dataset repository.
2. Azure Data Factory uses an HTTP linked service, Lookup, ForEach, and parameterized Copy Activity to land files in ADLS Gen2 Bronze.
3. Azure Databricks reads Bronze data and applies PySpark transformations into Silver.
4. Azure Synapse Serverless SQL queries Silver Parquet files with OPENROWSET and exposes Gold-layer views.
5. Power BI can consume the curated views (the supplied document describes downstream use, but does not show a completed dashboard).

## Lakehouse layers
| Layer | Purpose | Documented implementation |
|---|---|---|
| Bronze | Preserve source data | Raw CSV files copied to ADLS Gen2 |
| Silver | Clean and conform | PySpark transformations written to Silver |
| Gold | Serve analytics | Synapse Serverless SQL views over Silver Parquet |

## Documented transformations
- Calendar: derive Month and Year from Date.
- Customers: concatenate name fields into FullName and drop source name fields.
- Products: derive ProductSize from ProductSKU and fill missing values with Not Applicable.
- Sales: aggregate OrderQuantity by TerritoryKey; replace the SO prefix in order numbers; derive an order-line quantity; convert OrderDate to timestamp.
- Analytics examples: territory-wise performance and month/year sales analysis.

## Security in the supplied document
The walkthrough uses an Entra ID application / service principal to connect Databricks to ADLS and grants Storage Blob Data Contributor. It also describes a managed identity for Synapse access. It does not document Unity Catalog or Databricks Access Connector configuration.

## Not documented / future enhancements
- Watermark-based incremental ingestion and CDC
- Explicit schema contracts and automated schema-drift handling
- Quarantine/reject path and comprehensive automated data-quality framework
- Delta MERGE / SCD Type 2 handling
- Formal fact/dimension star schema and tested semantic model
- Power BI dashboard implementation and refresh configuration
- CI/CD, monitoring/alerting, and cost/performance benchmarks