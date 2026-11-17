# Databricks / PySpark notebook: AdventureWorks Bronze ingestion
from pyspark.sql import functions as F
from pathlib import Path

# Download the ten source CSVs into this folder before running locally.
# In Azure, replace these paths with ADLS Gen2 locations.
SOURCE_DIR = "data/raw"
BRONZE_DIR = "data/bronze"

source_files = [
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

# Production note: prefer explicit schemas, a run ID, and an idempotent
# write strategy. This local starter writes Delta; the supplied walkthrough
# describes raw CSV landing in ADLS Bronze.
