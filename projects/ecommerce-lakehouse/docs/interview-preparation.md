# E-Commerce Lakehouse — interview preparation

## Resume-supported explanation
"I worked on an e-commerce lakehouse pipeline where Azure Data Factory ingested source data into ADLS Gen2. The data was processed in a Microsoft Fabric Lakehouse using Fabric Notebooks with PySpark and Spark SQL. I organized the processing into Bronze, Silver and Gold Delta layers, applying cleansing, deduplication, aggregation and data-quality checks."

Only claim hands-on steps you have personally executed and can demonstrate.

## Be ready to explain
- Why separate Bronze, Silver and Gold?
- How does ADF land data into ADLS Gen2?
- How does a Fabric Lakehouse store and expose Delta tables?
- How do PySpark and Spark SQL fit into notebook transformations?
- How would you define a business key for deduplication?
- How do you make notebook reruns idempotent?
- Which data-quality checks run before promoting Silver to Gold?
- How would you monitor a Fabric pipeline and notebook run?

## Still to confirm
Exact source dataset, schema, keys, incremental load design, KPIs, and report output.
