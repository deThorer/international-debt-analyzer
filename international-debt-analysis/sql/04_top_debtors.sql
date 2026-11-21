-- Q4. Top 10 countries by total debt (naive and de-duplicated totals).
SELECT
    d.country_name,
    ROUND(SUM(d.debt) / 1e9, 2)                                     AS naive_total_bn_usd,
    ROUND(SUM(CASE WHEN i.level = 1 THEN d.debt END) / 1e9, 2)    AS dedup_total_bn_usd,
    COUNT(*)                                                        AS indicators_reported
FROM countries_debt AS d
JOIN indicators     AS i USING (indicator_code)
GROUP BY d.country_name
ORDER BY naive_total_bn_usd DESC
LIMIT 10;
