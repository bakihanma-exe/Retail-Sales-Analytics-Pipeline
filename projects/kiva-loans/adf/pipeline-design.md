# ADF pipeline design

## Pipeline 1 — Copy all dbo tables to Bronze
1. Linked service to on-prem SQL Server using Self-Hosted Integration Runtime.
2. Store SQL credentials in Azure Key Vault; use ADF managed identity to retrieve secrets.
3. Linked service to ADLS Gen2.
4. Lookup activity executes the metadata query in `sql/metadata_tables.sql`.
5. ForEach items: `@activity('LookupTables').output.value`.
6. Inside ForEach, Copy Activity source query:
   `@concat('SELECT * FROM ', item().SchemaName, '.', item().TableName)`.
7. Sink to a per-table Bronze folder in CSV format.

## Pipeline 2 — Transform
After the ForEach ingestion succeeds:
- Databricks notebook activity: Bronze to Silver.
- On success, Databricks notebook activity: Silver to Gold.

## Pipeline 3 — Publish Synapse views
- Get Metadata lists Gold table folders.
- ForEach calls the Synapse stored procedure with the current folder/table name.
- Use a managed identity for Synapse-to-storage access as supported by the workspace configuration.

## Trigger / operational notes
The source walkthrough uses a daily trigger. It describes overwriting Bronze on each run. That is a full refresh pattern, not a durable incremental load. If incremental ingestion is required, add a source watermark/CDC strategy and update the watermark only after successful copy. The supplied document does not show that implementation.
