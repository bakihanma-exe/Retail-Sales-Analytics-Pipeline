# Databricks / PySpark notebook: AdventureWorks Bronze ingestion
# Raw landing is a full-file refresh: reruns replace each table's Bronze snapshot.
# For a true incremental design, implement a verified source watermark/CDC first.
from pathlib import Path
from pyspark.sql import functions as F

SOURCE_DIR = "data/raw"       # Replace with abfss://.../bronze landing in Azure
BRONZE_DIR = "data/bronze"    # Replace with abfss://.../bronze_delta in Azure

SOURCE_FILES = [
    "AdventureWorks_Calendar.csv",
    "AdventureWorks_Customers.csv",
    "AdventureWorks_Product_Categories.csv",
    "AdventureWorks_Product_Subcategories.csv",
    "AdventureWorks_Products.csv",
    "AdventureWorks_Returns.csv",
    "AdventureWorks_Sales_2015.csv",
    "AdventureWorks_Sales_2016.csv",
    "AdventureWorks_Sales_2017.csv",
    "AdventureWorks_Territories.csv",
]

for file_name in SOURCE_FILES:
    source_path = f"{SOURCE_DIR}/{file_name}"
    table_name = Path(file_name).stem.lower()

    # Keep raw values as strings in Bronze. Type conversion belongs in Silver.
    df = (spark.read
          .option("header", True)
          .option("inferSchema", False)
          .option("mode", "FAILFAST")
          .csv(source_path))

    if not df.columns:
        raise ValueError(f"No CSV header found: {source_path}")

    bronze_df = (df
        .withColumn("_source_file", F.input_file_name())
        .withColumn("_ingested_at_utc", F.current_timestamp()))

    target_path = f"{BRONZE_DIR}/{table_name}"
    (bronze_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(target_path))

    print(f"Bronze refreshed: {table_name}; rows={bronze_df.count()}")

# This is an idempotent full-refresh pattern for a static dataset snapshot.
# Do not switch to append without a stable batch identifier and duplicate policy.
