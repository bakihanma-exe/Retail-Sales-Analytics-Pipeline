# E-Commerce Lakehouse architecture

## Resume-documented flow
E-Commerce source data → Azure Data Factory → ADLS Gen2 → Microsoft Fabric Lakehouse → Fabric Notebooks (PySpark / Spark SQL) → Bronze / Silver / Gold Delta layers.

## Layer responsibilities
- Bronze: source-aligned raw ingestion with load metadata.
- Silver: data type standardization, null handling, deduplication and validation.
- Gold: business aggregates for reporting.

## Unconfirmed details
The resume does not specify the source platform, file format, dataset name, schema, incremental strategy, orchestration trigger, Fabric workspace configuration, or report/dashboard. Confirm these before treating the design as a concrete implementation.
