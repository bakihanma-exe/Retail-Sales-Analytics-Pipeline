# Microsoft Fabric notebook template — Gold aggregation
from pyspark.sql import functions as F

SILVER_TABLE = "silver_ecommerce"
GOLD_TABLE = "gold_ecommerce_summary"

df = spark.table(SILVER_TABLE)

# This generic count is a placeholder until the real e-commerce schema
# and agreed business metrics are supplied.
gold_df = df.agg(
    F.count("*").alias("record_count")
)

(gold_df.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLE))

display(gold_df)
