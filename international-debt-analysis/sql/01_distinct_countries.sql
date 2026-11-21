-- Q1. How many distinct countries are in the data?
-- Aggregates (regions / income groups) are excluded through the countries_debt view.
SELECT COUNT(DISTINCT country_name) AS total_distinct_countries
FROM countries_debt;
