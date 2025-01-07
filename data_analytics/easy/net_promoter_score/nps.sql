WITH months AS (
    SELECT
        date_trunc('month', score_date)::date AS month
    FROM
        customer_feedback
    WHERE
        extract(year from score_date) = 2023
    GROUP BY
        month
),
extend_feedback AS (
    SELECT
        m.month,
        f.user_id,
        f.score,
        f.score_date
    FROM
        months m
    LEFT JOIN
    customer_feedback f on f.score_date between m.month - interval '90 days' AND m.month +  interval '30 days'
),
last_scores_in_month AS (
    SELECT DISTINCT ON (user_id, month)
        user_id,
        month,
        score AS last_score
    FROM
        extend_feedback
    ORDER BY
        user_id,
        month,
        score_date DESC
),
nps_calcs AS (
    SELECT
        month,
        COUNT(1) FILTER (WHERE last_score >= 9)::float AS promoter_ct,
        COUNT(1) FILTER (WHERE last_score <= 6)::float AS detractor_ct,
        COUNT(1)::float AS all_responses_ct
    FROM
        last_scores_in_month
    GROUP BY
        month
    ORDER BY
        month
)
SELECT
    month,
    ROUND(CAST(((promoter_ct/all_responses_ct) - (detractor_ct/all_responses_ct)) * 100.00 AS numeric), 2) AS nps
FROM
    nps_calcs;
