-- AdventureWorks data quality checks (Databricks SQL / Spark SQL).
-- Table and column names reflect the normalized snake_case Silver outputs.

-- Null product keys in sales
SELECT COUNT(*) AS null_product_keys
FROM silver.sales
WHERE product_key IS NULL;

-- Duplicate sales rows by natural row grain
SELECT order_number, order_line_item, COUNT(*) AS duplicate_count
FROM silver.sales
GROUP BY order_number, order_line_item
HAVING COUNT(*) > 1;

-- Invalid order dates
SELECT COUNT(*) AS invalid_order_dates
FROM silver.sales
WHERE order_date IS NULL;

-- Orphan product references
SELECT COUNT(*) AS orphan_product_keys
FROM silver.sales s
LEFT JOIN silver.products p ON s.product_key = p.product_key
WHERE p.product_key IS NULL;

-- Negative / zero quantities (review business meaning before rejecting)
SELECT COUNT(*) AS non_positive_quantities
FROM silver.sales
WHERE order_quantity <= 0;

-- Returns should have non-negative quantities in this dataset
SELECT COUNT(*) AS invalid_return_quantities
FROM silver.returns
WHERE return_quantity < 0;
