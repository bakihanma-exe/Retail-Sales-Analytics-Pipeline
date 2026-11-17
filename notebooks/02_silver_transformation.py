# Databricks / PySpark notebook: Silver transformation helpers
from pyspark.sql import functions as F
from pyspark.sql.window import Window

BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"

def clean_column_names(df):
    """Normalize column names for consistent downstream references."""
    for old_name in df.columns:
        new_name = (old_name.strip().lower()
                    .replace(" ", "_").replace("-", "_"))
        if old_name != new_name:
            df = df.withColumnRenamed(old_name, new_name)
    return df

def trim_string_columns(df):
    for field in df.schema.fields:
        if field.dataType.simpleString() == "string":
            df = df.withColumn(field.name, F.trim(F.col(field.name)))
    return df

def currency_to_decimal(df, column_name):
    """Remove currency symbols/commas and cast to a decimal."""
    cleaned = F.regexp_replace(F.col(column_name), r"[$,]", "")
    return df.withColumn(column_name, cleaned.cast("decimal(18,2)"))

def parse_date_column(df, column_name, fmt="yyyy-MM-dd"):
    return df.withColumn(column_name, F.to_date(F.col(column_name), fmt))

def deduplicate_by_key(df, key_columns, order_column=None):
    """Keep the latest record per key when an ordering column is supplied."""
    if not order_column:
        return df.dropDuplicates(key_columns)
    w = Window.partitionBy(*key_columns).orderBy(F.col(order_column).desc_nulls_last())
    return (df.withColumn("_rn", F.row_number().over(w))
              .filter(F.col("_rn") == 1)
              .drop("_rn"))

# Example: adapt table name, keys, and date/amount columns to your dataset.
# sales = spark.read.format("delta").load(f"{BRONZE_DIR}/sales")
# sales = clean_column_names(sales)
# sales = trim_string_columns(sales)
# sales = currency_to_decimal(sales, "sales_amount")
# sales = parse_date_column(sales, "order_date")
# sales = deduplicate_by_key(sales, ["sales_id"], "modified_date")
# sales.write.format("delta").mode("overwrite").save(f"{SILVER_DIR}/sales")
