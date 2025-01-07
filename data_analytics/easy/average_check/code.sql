SELECT
    DATE_TRUNC('month', toDate(buy_date)) ::DATE AS month,
    AVG(check_amount) AS avg_check,
    arrayElement(quantilesExactExclusive(0.5)(check_amount), 1) as median_check
FROM
    view_checks
GROUP BY
    month
ORDER BY
    month;
