-- Q5. Average amount per indicator, highest first.
SELECT
    indicator_code                  AS debt_indicator,
    indicator_name,
    ROUND(AVG(debt) / 1e6, 2)       AS average_debt_million_usd,
    COUNT(*)                        AS countries_reporting
FROM countries_debt
GROUP BY indicator_code, indicator_name
ORDER BY average_debt_million_usd DESC
LIMIT 10;
