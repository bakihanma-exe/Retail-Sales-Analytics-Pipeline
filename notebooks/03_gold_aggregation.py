# Databricks / PySpark notebook: AdventureWorks Gold aggregations
from pyspark.sql import functions as F
from pyspark.sql.window import Window

SILVER_DIR = "data/silver"
GOLD_DIR = "data/gold"

sales = spark.read.format("delta").load(f"{SILVER_DIR}/sales")
products = spark.read.format("delta").load(f"{SILVER_DIR}/products")
subcategories = spark.read.format("delta").load(f"{SILVER_DIR}/product_subcategories")
categories = spark.read.format("delta").load(f"{SILVER_DIR}/product_categories")
territories = spark.read.format("delta").load(f"{SILVER_DIR}/territories")

# Sales source has quantity but no sales amount. Estimate gross sales using ProductPrice.
product_hierarchy = (products
    .join(subcategories, "product_subcategory_key", "left")
    .join(categories, "product_category_key", "left"))

sales_enriched = (sales
    .join(product_hierarchy, "product_key", "left")
    .join(territories, sales["territory_key"] == territories["sales_territory_key"], "left")
    .withColumn("estimated_gross_sales",
                F.col("product_price").cast("double") * F.col("order_quantity").cast("double")))

# Monthly / yearly quantity and estimated gross sales.
monthly_sales = (sales_enriched
    .withColumn("order_year", F.year("order_date"))
    .withColumn("order_month", F.month("order_date"))
    .groupBy("order_year", "order_month")
    .agg(F.sum("order_quantity").alias("total_quantity"),
         F.sum("estimated_gross_sales").alias("estimated_gross_sales")))

monthly_sales.write.format("delta").mode("overwrite").save(f"{GOLD_DIR}/monthly_sales")

# Territory performance as described in the source walkthrough.
territory_sales = (sales_enriched
    .groupBy("territory_key", "region", "country", "continent")
    .agg(F.sum("order_quantity").alias("total_order_quantity"),
         F.sum("estimated_gross_sales").alias("estimated_gross_sales")))

territory_sales.write.format("delta").mode("overwrite").save(f"{GOLD_DIR}/territory_performance")

# Product/category ranking (extension to the source document).
category_product_sales = (sales_enriched
    .groupBy("category_name", "subcategory_name", "product_name")
    .agg(F.sum("estimated_gross_sales").alias("estimated_gross_sales")))

w = Window.partitionBy("category_name").orderBy(F.col("estimated_gross_sales").desc())
top_products = (category_product_sales
    .withColumn("sales_rank", F.dense_rank().over(w))
    .filter(F.col("sales_rank") <= 5))

top_products.write.format("delta").mode("overwrite").save(f"{GOLD_DIR}/top_products_by_category")

# Returns overview; returns are counts/quantities, not negative sales rows.
returns = spark.read.format("delta").load(f"{SILVER_DIR}/returns")
returns_summary = (returns.groupBy("territory_key", "product_key")
    .agg(F.sum("return_quantity").alias("total_return_quantity")))
returns_summary.write.format("delta").mode("overwrite").save(f"{GOLD_DIR}/returns_summary")
