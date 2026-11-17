-- Adapt table and column names to the source dataset before execution.

-- 1. Null business keys
SELECT COUNT(*) AS null_key_count
FROM SilverSales
WHERE SalesID IS NULL;

-- 2. Duplicate business keys
SELECT SalesID, COUNT(*) AS duplicate_count
FROM SilverSales
GROUP BY SalesID
HAVING COUNT(*) > 1;

-- 3. Invalid negative amounts (confirm whether returns are represented as negatives)
SELECT COUNT(*) AS negative_amount_count
FROM SilverSales
WHERE SalesAmount < 0;

-- 4. Null / invalid dates
SELECT COUNT(*) AS invalid_date_count
FROM SilverSales
WHERE OrderDate IS NULL;

-- 5. Orphan product references
SELECT COUNT(*) AS orphan_product_count
FROM SilverSales s
LEFT JOIN SilverProduct p ON s.ProductKey = p.ProductKey
WHERE p.ProductKey IS NULL;
