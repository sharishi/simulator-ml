SELECT
    DATE_TRUNC('month', date) ::DATE AS time,
    SUM(amount) / COUNT(distinct email_id) AS arppu,
    AVG(amount) AS aov
    FROM
    new_payments
    WHERE
    status = 'Confirmed'
GROUP BY
    DATE_TRUNC('month', date)
ORDER BY
    time;