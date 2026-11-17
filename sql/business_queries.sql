-- Adapt names and metrics to the confirmed Silver / Gold schema.

-- Monthly sales trend
SELECT
    YEAR(OrderDate) AS sales_year,
    MONTH(OrderDate) AS sales_month,
    SUM(SalesAmount) AS total_sales
FROM SilverSales
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY sales_year, sales_month;

-- Sales by product category
SELECT
    p.Category,
    SUM(s.SalesAmount) AS total_sales
FROM SilverSales s
JOIN SilverProduct p ON s.ProductKey = p.ProductKey
GROUP BY p.Category
ORDER BY total_sales DESC;

-- Top 5 products in each category (ties receive the same rank)
WITH product_sales AS (
    SELECT p.Category, p.ProductName, SUM(s.SalesAmount) AS total_sales
    FROM SilverSales s
    JOIN SilverProduct p ON s.ProductKey = p.ProductKey
    GROUP BY p.Category, p.ProductName
),
ranked AS (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY Category ORDER BY total_sales DESC) AS sales_rank
    FROM product_sales
)
SELECT Category, ProductName, total_sales, sales_rank
FROM ranked
WHERE sales_rank <= 5
ORDER BY Category, sales_rank;

-- Sales versus target: confirm grain and target allocation before joining
-- to avoid multiplying sales rows.
