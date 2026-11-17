# Microsoft Fabric notebook template — Silver cleansing
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_TABLE = "bronze_ecommerce"
SILVER_TABLE = "silver_ecommerce"

df = spark.table(BRONZE_TABLE)

# Normalize column names to snake_case.
import re
for old_name in df.columns:
    new_name = re.sub(r"[^A-Za-z0-9]+", "_", old_name.strip()).strip("_").lower()
    if old_name != new_name:
        df = df.withColumnRenamed(old_name, new_name)

# Trim string columns.
for field in df.schema.fields:
    if field.dataType.simpleString() == "string":
        df = df.withColumn(field.name, F.trim(F.col(field.name)))

# Example deduplication template — replace with the actual business key
# and deterministic latest-update column after schema discovery.
# window = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc_nulls_last())
# df = (df.withColumn("_rn", F.row_number().over(window))
#         .filter(F.col("_rn") == 1).drop("_rn"))

(df.write.format("delta")
   .mode("overwrite")
   .option("overwriteSchema", "true")
   .saveAsTable(SILVER_TABLE))

print(f"Silver rows: {df.count()}")
