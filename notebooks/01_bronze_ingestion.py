# Databricks / PySpark notebook: Bronze ingestion starter
from pyspark.sql import functions as F
from pathlib import Path

# Change these paths for your workspace / ADLS Gen2 environment.
SOURCE_DIR = "data/raw"
BRONZE_DIR = "data/bronze"

source_files = [
    "Product.csv", "Region.csv", "Reseller.csv", "Sales.csv",
    "Salesperson.csv", "SalespersonRegion.csv", "Target.csv"
]

for file_name in source_files:
    source_path = f"{SOURCE_DIR}/{file_name}"
    table_name = Path(file_name).stem.lower()

    df = (spark.read
          .option("header", True)
          .option("inferSchema", True)
          .csv(source_path))

    bronze_df = (df
        .withColumn("_source_file", F.lit(file_name))
        .withColumn("_ingested_at_utc", F.current_timestamp())
        .withColumn("_load_date", F.current_date()))

    (bronze_df.write
        .format("delta")
        .mode("append")
        .partitionBy("_load_date")
        .save(f"{BRONZE_DIR}/{table_name}"))

    print(f"Ingested {file_name}: {bronze_df.count()} rows")

# Production note: use explicit schemas, cloud storage paths, run IDs,
# and idempotent batch handling instead of relying on inferSchema + append.
