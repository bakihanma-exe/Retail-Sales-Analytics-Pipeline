# Microsoft Fabric notebook template — Bronze ingestion
# Update source and Lakehouse paths to match the chosen e-commerce dataset.
from pyspark.sql import functions as F

SOURCE_PATH = "Files/landing/ecommerce/"
BRONZE_TABLE = "bronze_ecommerce"

raw_df = (spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(SOURCE_PATH))

bronze_df = (raw_df
    .withColumn("_ingested_at_utc", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name()))

(bronze_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(BRONZE_TABLE))

print(f"Bronze rows written: {bronze_df.count()}")

# Before production use: define an explicit schema, source manifest,
# stable batch ID and idempotent retry strategy.
