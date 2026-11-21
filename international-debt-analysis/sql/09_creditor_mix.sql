-- Q9. Who is the long-term debt owed to? Creditor mix by flow type.
-- Share of each level-2 creditor class in the long-term total (level 1).
-- If shares don't add to 100%, some child series are not reported (e.g. no DIS.DPNG).
WITH totals AS (
    SELECT i.flow_type, SUM(d.debt) AS long_term
    FROM countries_debt AS d
    JOIN indicators     AS i USING (indicator_code)
    WHERE i.level = 1
    GROUP BY i.flow_type
)
SELECT
    i.flow_type,
    i.creditor,
    ROUND(SUM(d.debt) / 1e9, 2)                     AS amount_bn_usd,
    ROUND(100.0 * SUM(d.debt) / t.long_term, 1)     AS pct_of_long_term
FROM countries_debt AS d
JOIN indicators     AS i USING (indicator_code)
JOIN totals         AS t ON t.flow_type = i.flow_type
WHERE i.level = 2
GROUP BY i.flow_type, i.creditor
ORDER BY i.flow_type, amount_bn_usd DESC;
