# E-Commerce Lakehouse Pipeline

This project folder is based on the scope stated in the uploaded resume. No separate E-Commerce implementation walkthrough or exact dataset schema was found in the uploaded project documents.

## Resume-documented scope
- Azure Data Factory ingests e-commerce data into ADLS Gen2.
- Microsoft Fabric Lakehouse is the processing environment.
- Fabric Notebooks use PySpark and Spark SQL.
- Cleansing, deduplication, aggregation and data-quality checks.
- Data is organized into Bronze, Silver and Gold Delta layers.

## Planned folder contents
- `adf/`: ingestion pipeline design and parameters
- `notebooks/`: Fabric-compatible Bronze, Silver and Gold notebook templates
- `sql/`: Spark SQL transformations and validation queries
- `docs/`: architecture, assumptions and interview preparation
- `tests/`: schema and quality checks

## Important
The source material does not identify the exact e-commerce dataset, column names, source system, or business KPIs. The templates in this folder are clearly marked as adaptable examples until a dataset is selected and its schema is verified. Do not describe them as a deployed production pipeline.
