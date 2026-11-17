# Databricks / PySpark notebook: Gold business aggregates
from pyspark.sql import functions as F
from pyspark.sql.window import Window

SILVER_DIR = "data/silver"
GOLD_DIR = "data/gold"

# Adapt these column names to the actual dataset schema.
sales = spark.read.format("delta").load(f"{SILVER_DIR}/sales")
products = spark.read.format("delta").load(f"{SILVER_DIR}/product")

# Example category / subcategory sales summary.
sales_product = sales.join(products, on="product_key", how="inner")

category_summary = (sales_product
    .groupBy("category", "subcategory")
    .agg(
        F.sum("sales_amount").alias("total_sales"),
        F.avg("sales_amount").alias("average_sales"),
        F.count("*").alias("transaction_count")
    ))

(category_summary.write.format("delta")
 .mode("overwrite").save(f"{GOLD_DIR}/category_summary"))

# Top 5 products per category using dense_rank (ties share the same rank).
product_sales = (sales_product.groupBy("category", "product_name")
                 .agg(F.sum("sales_amount").alias("total_sales")))

w = Window.partitionBy("category").orderBy(F.col("total_sales").desc())
top_products = (product_sales
    .withColumn("sales_rank", F.dense_rank().over(w))
    .filter(F.col("sales_rank") <= 5))

(top_products.write.format("delta")
 .mode("overwrite").save(f"{GOLD_DIR}/top_products_by_category"))

# Validate the actual key names and monetary definition before running.
