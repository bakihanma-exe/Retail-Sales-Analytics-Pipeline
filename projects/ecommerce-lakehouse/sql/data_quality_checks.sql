-- Fabric Spark SQL template. Replace example fields after confirming schema.

-- Row count
SELECT COUNT(*) AS row_count FROM silver_ecommerce;

-- Null checks (replace order_id with the confirmed business key)
-- SELECT COUNT(*) AS null_order_ids
-- FROM silver_ecommerce WHERE order_id IS NULL;

-- Duplicate check (replace with actual key)
-- SELECT order_id, COUNT(*) AS duplicate_count
-- FROM silver_ecommerce
-- GROUP BY order_id
-- HAVING COUNT(*) > 1;
