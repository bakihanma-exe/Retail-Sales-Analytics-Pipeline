"""Reusable PySpark data-quality checks.
Run against a DataFrame after adapting the required column names.
"""
from pyspark.sql import functions as F

def assert_no_nulls(df, columns):
    failures = {}
    for column in columns:
        count = df.filter(F.col(column).isNull()).count()
        if count:
            failures[column] = count
    if failures:
        raise AssertionError(f"Null values found: {failures}")

def assert_unique_key(df, key_columns):
    duplicates = (df.groupBy(*key_columns)
                    .count()
                    .filter(F.col("count") > 1))
    sample = duplicates.limit(10).collect()
    if sample:
        raise AssertionError(f"Duplicate keys found (sample): {sample}")

def assert_non_negative(df, column):
    invalid_count = df.filter(F.col(column) < 0).count()
    if invalid_count:
        raise AssertionError(f"{invalid_count} negative values in {column}")

# Example:
# assert_no_nulls(sales_df, ["sales_id", "product_key", "order_date"])
# assert_unique_key(sales_df, ["sales_id"])
# assert_non_negative(sales_df, "sales_amount")
