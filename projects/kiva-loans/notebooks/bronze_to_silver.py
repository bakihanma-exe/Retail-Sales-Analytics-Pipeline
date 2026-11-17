# Databricks notebook: Bronze to Silver (Kiva walkthrough pattern)
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, TimestampType
import re

BRONZE_ROOT = "/mnt/bronze/dbo"
SILVER_ROOT = "/mnt/silver/dbo"

def normalize_date_time_columns(df):
    for field in df.schema.fields:
        name = field.name.lower()
        if "date" in name or "time" in name:
            # Preserve a date type where source values are date-like.
            # TimestampType values are formatted only if the downstream
            # contract explicitly requires a yyyy-MM-dd string.
            if isinstance(field.dataType, DateType):
                df = df.withColumn(field.name, F.to_date(F.col(field.name)))
            elif isinstance(field.dataType, TimestampType):
                df = df.withColumn(field.name, F.to_date(F.col(field.name)))
    return df

table_names = [
    item.name.rstrip("/")
    for item in dbutils.fs.ls(BRONZE_ROOT)
    if item.isDir()
]

for table_name in table_names:
    input_path = f"{BRONZE_ROOT}/{table_name}/{table_name}.csv"
    df = (spark.read.format("csv")
          .option("header", "true")
          .option("inferSchema", "true")
          .load(input_path))
    silver_df = normalize_date_time_columns(df)
    output_path = f"{SILVER_ROOT}/{table_name}/"
    (silver_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(output_path))
    print(f"Silver written: {table_name}, rows={silver_df.count()}")

# Note: The source walkthrough writes CSV in Silver. This reconstruction
# uses Delta as a deliberate improvement; update downstream readers accordingly.
