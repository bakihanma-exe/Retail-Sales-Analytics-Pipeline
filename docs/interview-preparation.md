# Interview preparation notes

## 60-second project explanation
"I designed a retail sales analytics pipeline that ingests multiple retail entities through Azure Data Factory using a watermark-based incremental pattern. The raw extracts land in ADLS Gen2 Bronze. Databricks with PySpark standardizes data types, trims text, handles date and currency fields, removes duplicates, and applies data-quality checks in Silver. Gold contains business aggregates such as category sales and top products per category using window functions. Power BI can use the curated Gold outputs for sales trends, regional performance, and sales-versus-target reporting."

Only describe steps you have personally implemented and can demonstrate. If discussing this repository before deploying it, call it a portfolio implementation / reference build rather than a production deployment.

## Common interview questions
1. Why use a watermark? To extract only records changed since the prior successful load.
2. When should a watermark advance? Only after the corresponding ingestion succeeds.
3. What is the Bronze layer? A source-faithful landing layer with ingestion metadata.
4. What happens in Silver? Standardization, cleansing, deduplication, and quality validation.
5. What belongs in Gold? Curated business-level facts, dimensions, and aggregates.
6. Why Delta Lake? It adds transactional reliability and features such as MERGE and time travel to lake storage.
7. DENSE_RANK versus ROW_NUMBER? DENSE_RANK preserves ties without gaps; ROW_NUMBER assigns a unique sequence.
8. How do you handle duplicates? Define a business key and deterministic ordering, then deduplicate or MERGE.
9. What if a pipeline fails? Do not update the watermark; retry safely and make sink writes idempotent.
10. How would you optimize Spark? Filter early, select needed columns, avoid unnecessary shuffles, broadcast small dimensions when appropriate, and inspect the execution plan.

## Be ready to explain
- Exact source schema and business keys
- Watermark control table and failure handling
- Incremental versus full load
- Delta MERGE / deduplication strategy
- Partitioning and small-file management
- Data quality rules and rejected-record handling
- Unity Catalog external locations and managed identity
- Gold model grain and Power BI relationships
