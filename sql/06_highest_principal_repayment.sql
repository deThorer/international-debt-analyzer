-- Q6. Which country made the largest long-term principal repayment?
SELECT country_name, indicator_name, ROUND(debt / 1e9, 2) AS amount_bn_usd
FROM countries_debt
WHERE debt = (SELECT MAX(debt)
              FROM countries_debt
              WHERE indicator_code = 'DT.AMT.DLXF.CD')
  AND indicator_code = 'DT.AMT.DLXF.CD';
