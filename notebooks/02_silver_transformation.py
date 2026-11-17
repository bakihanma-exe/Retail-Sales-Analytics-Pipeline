# Databricks / PySpark notebook: AdventureWorks Silver transformations
import re
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"

def clean_column_names(df):
    """Convert CamelCase / spaces to snake_case."""
    for old_name in df.columns:
        new_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", old_name.strip())
        new_name = re.sub(r"[^A-Za-z0-9]+", "_", new_name).strip("_").lower()
        if old_name != new_name:
            df = df.withColumnRenamed(old_name, new_name)
    return df

spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

def write_delta(df, name):
    (df.write.format("delta").mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(f"silver.{name}"))

# Calendar: source Date values are M/d/yyyy (example: 1/1/2015).
calendar = clean_column_names(spark.read.format("delta").load(f"{BRONZE_DIR}/adventureworks_calendar"))
calendar = (calendar
    .withColumn("date", F.to_date("date", "M/d/yyyy"))
    .withColumn("month", F.month("date"))
    .withColumn("year", F.year("date")))
write_delta(calendar, "calendar")

# Customers: the source document describes FullName = Prefix + FirstName + LastName.
customers = clean_column_names(spark.read.format("delta").load(f"{BRONZE_DIR}/adventureworks_customers"))
customer_columns = set(customers.columns)
name_parts = [c for c in ["prefix", "firstname", "lastname"] if c in customer_columns]
# After snake_case normalization these names become prefix, first_name, last_name.
name_parts = [c for c in ["prefix", "first_name", "last_name"] if c in customer_columns]
if "first_name" in customer_columns and "last_name" in customer_columns:
    pieces = [F.col(c) for c in name_parts]
    customers = customers.withColumn("full_name", F.concat_ws(" ", *pieces))
    customers = customers.drop(*[c for c in ["prefix", "first_name", "last_name"] if c in customers.columns])
write_delta(customers, "customers")

# Product: retain source columns and derive size from ProductSKU where possible.
products = clean_column_names(spark.read.format("delta").load(f"{BRONZE_DIR}/adventureworks_products"))
if "product_sku" in products.columns:
    products = products.withColumn(
        "derived_product_size",
        F.when(F.regexp_extract("product_sku", r"-([A-Z0-9]+)$", 1) != "",
               F.regexp_extract("product_sku", r"-([A-Z0-9]+)$", 1))
         .otherwise(F.lit("Not Applicable"))
    )
if "product_size" in products.columns:
    products = products.withColumn("product_size", F.when(
        F.col("product_size").isNull() | (F.trim(F.col("product_size")) == "") | (F.col("product_size") == "0"),
        F.lit("Not Applicable")).otherwise(F.col("product_size")))
write_delta(products, "products")

# Small reference entities.
for source_name, target_name in [
    ("adventureworks_product_categories", "product_categories"),
    ("adventureworks_product_subcategories", "product_subcategories"),
    ("adventureworks_territories", "territories"),
    ("adventureworks_returns", "returns"),
]:
    df = clean_column_names(spark.read.format("delta").load(f"{BRONZE_DIR}/{source_name}"))
    write_delta(df, target_name)

# Sales: combine yearly files, normalize order number, derive line quantity and timestamp.
sales_paths = [
    f"{BRONZE_DIR}/adventureworks_sales_2015",
    f"{BRONZE_DIR}/adventureworks_sales_2016",
    f"{BRONZE_DIR}/adventureworks_sales_2017",
]
sales_frames = [clean_column_names(spark.read.format("delta").load(p)) for p in sales_paths]
sales = sales_frames[0]
for frame in sales_frames[1:]:
    sales = sales.unionByName(frame, allowMissingColumns=True)

sales = (sales
    .withColumn("order_number", F.regexp_replace("order_number", r"^SO", "ON"))
    .withColumn("order_date", F.to_timestamp("order_date", "M/d/yyyy"))
    .withColumn("stock_date", F.to_timestamp("stock_date", "M/d/yyyy"))
    .withColumn("order_line_quantity", F.col("order_line_item").cast("int") * F.col("order_quantity").cast("int")))
write_delta(sales, "sales")

# Production improvement: add explicit schemas, quarantine invalid rows,
# deterministic duplicate rules, and idempotent Delta MERGE where appropriate.
