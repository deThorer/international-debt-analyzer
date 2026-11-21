-- Q11. Breakdown for the top debtor (China) by flow type.
SELECT
    i.flow_type,
    COUNT(*)                                AS indicators,
    ROUND(SUM(d.debt) / 1e9, 2)             AS naive_bn_usd,
    ROUND(SUM(CASE WHEN i.level = 1 THEN d.debt END) / 1e9, 2) AS dedup_bn_usd
FROM countries_debt AS d
JOIN indicators     AS i USING (indicator_code)
WHERE d.country_name = 'China'
GROUP BY i.flow_type
ORDER BY naive_bn_usd DESC;
