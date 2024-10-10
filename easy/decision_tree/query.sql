SELECT
    age,
    income,
    dependents,
    has_property,
    has_car,
    credit_score,
    job_tenure,
    has_education,
    loan_amount,
    dateDiff('day', loan_start, loan_deadline) AS loan_period,
    CASE
        WHEN loan_payed > loan_deadline
        THEN dateDiff('day', loan_deadline, loan_payed)
        ELSE 0
    END AS delay_days
FROM
    default.loan_delay_days
ORDER BY
    id;

