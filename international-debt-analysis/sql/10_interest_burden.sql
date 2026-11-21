-- Q10. Interest paid per dollar of principal repaid (long-term debt).
-- A high ratio means a country is paying a lot just to service its debt.
WITH p AS (
    SELECT
        country_name,
        SUM(CASE WHEN indicator_code = 'DT.INT.DLXF.CD' THEN debt END) AS interest,
        SUM(CASE WHEN indicator_code = 'DT.AMT.DLXF.CD' THEN debt END) AS principal
    FROM countries_debt
    GROUP BY country_name
)
SELECT
    country_name,
    ROUND(interest / 1e9, 2)                AS interest_bn_usd,
    ROUND(principal / 1e9, 2)               AS principal_bn_usd,
    ROUND(interest / principal, 3)          AS interest_to_principal
FROM p
WHERE principal > 1e9            -- ignore very small borrowers, ratios get noisy
ORDER BY interest_to_principal DESC
LIMIT 10;
