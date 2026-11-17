# Databricks notebook: Silver to Gold (Kiva walkthrough pattern)
import re

SILVER_ROOT = "/mnt/silver/dbo"
GOLD_ROOT = "/mnt/gold/dbo"

table_names = [
    item.name.rstrip("/")
    for item in dbutils.fs.ls(SILVER_ROOT)
    if item.isDir()
]

def to_snake_case(name):
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name.strip())
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()

for table_name in table_names:
    input_path = f"{SILVER_ROOT}/{table_name}/"
    df = spark.read.format("delta").load(input_path)

    for old_name in df.columns:
        new_name = to_snake_case(old_name)
        if old_name != new_name:
            df = df.withColumnRenamed(old_name, new_name)

    output_path = f"{GOLD_ROOT}/{table_name}/"
    (df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(output_path))
    print(f"Gold written: {table_name}, rows={df.count()}")

# This follows the source walkthrough's column-name normalization.
# Add business-specific facts/dimensions only after inspecting the real schema.
