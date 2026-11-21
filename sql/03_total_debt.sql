-- Q3. Total amount of debt (in millions of US$).
-- naive_total sums every indicator (the usual approach, but it double counts because
-- parent series such as "long-term" already include their children).
-- dedup_total only sums the lowest level of the hierarchy.
SELECT
    ROUND(SUM(d.debt) / 1e6, 2)                                     AS naive_total_million_usd,
    ROUND(SUM(CASE WHEN i.level = 1 THEN d.debt END) / 1e6, 2)    AS dedup_total_million_usd
FROM countries_debt AS d
JOIN indicators     AS i USING (indicator_code);
