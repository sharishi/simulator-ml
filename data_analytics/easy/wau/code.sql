SELECT
    DISTINCT day,
    COUNT(DISTINCT user_id) OVER (
        ORDER BY day
        RANGE BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS wau
FROM (
    SELECT
        toDate(timestamp) AS day,
        user_id
    FROM
        default.churn_submits
) AS subquery
ORDER BY
    day;


