-- Q7. Which indicators are reported by the most countries?
-- Indicators reported by fewer countries are worth flagging: comparisons on them are less fair.
SELECT indicator_code, COUNT(*) AS indicator_count
FROM countries_debt
GROUP BY indicator_code
ORDER BY indicator_count DESC, indicator_code
LIMIT 20;
