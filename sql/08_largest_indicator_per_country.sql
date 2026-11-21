-- Q8. For each of the top 10 debtors, which single indicator is largest?
-- Uses a window function (ROW_NUMBER) to rank indicators inside each country.
WITH top_countries AS (
    SELECT country_code
    FROM countries_debt
    GROUP BY country_code
    ORDER BY SUM(debt) DESC
    LIMIT 10
),
ranked AS (
    SELECT
        d.country_name,
        d.indicator_code,
        d.indicator_name,
        d.debt,
        ROW_NUMBER() OVER (PARTITION BY d.country_code ORDER BY d.debt DESC) AS rn
    FROM countries_debt AS d
    JOIN top_countries   AS t USING (country_code)
)
SELECT country_name, indicator_code, indicator_name, ROUND(debt / 1e9, 2) AS amount_bn_usd
FROM ranked
WHERE rn = 1
ORDER BY debt DESC;
