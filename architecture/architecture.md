# Architecture and design

## End-to-end flow
1. Retail CSV extracts are landed in a source location.
2. Azure Data Factory orchestrates incremental copy using a watermark.
3. Raw records are retained in the Bronze layer with ingestion metadata.
4. Databricks / PySpark standardizes types, cleans values, and applies quality rules in Silver.
5. Gold produces business aggregates and dimensional reporting tables.
6. Power BI consumes curated Gold outputs.

## Lakehouse layers
| Layer | Purpose | Typical contents |
|---|---|---|
| Bronze | Preserve source fidelity | Raw CSV-derived Delta tables, source file, ingestion timestamp |
| Silver | Clean and conform | Standardized dates, numeric types, deduplicated records, validated keys |
| Gold | Serve analytics | Sales summaries, product rankings, sales-versus-target metrics |

## Security design
Use a Databricks Access Connector with managed identity to access ADLS Gen2. Register storage through Unity Catalog external locations and grant least-privilege access to the required identities. Keep secrets out of notebooks and source control.

## Operational considerations
- Advance the watermark only after all intended copy work succeeds.
- Use a half-open incremental range: greater than the previous watermark and less than or equal to the new watermark.
- Make retries safe; avoid duplicate appends by using stable keys and Delta MERGE where appropriate.
- Monitor row counts, failed pipeline activities, and data freshness.
