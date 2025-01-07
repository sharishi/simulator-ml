SELECT DISTINCT DATE(timestamp) as day,
    count(distinct user_id) AS dau
FROM churn_submits
group by day