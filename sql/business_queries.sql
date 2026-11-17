-- AdventureWorks Silver / Gold examples.
-- These are Spark SQL / Databricks SQL style queries against the normalized tables.

-- Monthly quantity trend (the source sales files do not contain a sales amount).
SELECT YEAR(order_date) AS sales_year,
       MONTH(order_date) AS sales_month,
       SUM(order_quantity) AS total_quantity
FROM silver.sales
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY sales_year, sales_month;

-- Territory performance
SELECT t.region, t.country, SUM(s.order_quantity) AS total_order_quantity
FROM silver.sales s
LEFT JOIN silver.territories t ON s.territory_key = t.sales_territory_key
GROUP BY t.region, t.country
ORDER BY total_order_quantity DESC;

-- Estimated gross sales by category = ProductPrice * OrderQuantity.
SELECT c.category_name,
       SUM(p.product_price * s.order_quantity) AS estimated_gross_sales
FROM silver.sales s
JOIN silver.products p ON s.product_key = p.product_key
LEFT JOIN silver.product_subcategories sc
       ON p.product_subcategory_key = sc.product_subcategory_key
LEFT JOIN silver.product_categories c
       ON sc.product_category_key = c.product_category_key
GROUP BY c.category_name
ORDER BY estimated_gross_sales DESC;

-- Top 5 products per category, including ties.
WITH product_sales AS (
    SELECT c.category_name, p.product_name,
           SUM(p.product_price * s.order_quantity) AS estimated_gross_sales
    FROM silver.sales s
    JOIN silver.products p ON s.product_key = p.product_key
    LEFT JOIN silver.product_subcategories sc
           ON p.product_subcategory_key = sc.product_subcategory_key
    LEFT JOIN silver.product_categories c
           ON sc.product_category_key = c.product_category_key
    GROUP BY c.category_name, p.product_name
),
ranked AS (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY category_name ORDER BY estimated_gross_sales DESC) AS sales_rank
    FROM product_sales
)
SELECT * FROM ranked WHERE sales_rank <= 5
ORDER BY category_name, sales_rank;
