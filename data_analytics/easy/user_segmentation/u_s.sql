WITH user_amounts AS (
  SELECT email_id, SUM(amount) AS summary
  FROM new_payments
  WHERE mode IN ('MasterCard', 'МИР', 'Visa') and status = 'Confirmed'
  GROUP BY email_id
),
max_summary AS (
  SELECT MAX(summary) AS max_amount
  FROM user_amounts
),
user_amounts_with_max AS (
  SELECT ua.email_id, ua.summary, ms.max_amount
  FROM user_amounts ua
  CROSS JOIN max_summary ms
),
purchase_ranges AS (
  SELECT
    email_id,
    CASE
      WHEN summary < 20000 THEN '0-20000'
      WHEN summary < 40000 THEN '20000-40000'
      WHEN summary < 60000 THEN '40000-60000'
      WHEN summary < 80000 THEN '60000-80000'
      WHEN summary < 100000 THEN '80000-100000'
      ELSE CONCAT('100000-', CAST(CEIL(max_amount)  AS VARCHAR))
    END AS purchase_range,
    summary
  FROM user_amounts_with_max
)
SELECT
  purchase_range,
  COUNT(email_id) AS num_of_users
FROM (
  SELECT
    CASE
      WHEN summary <= 20000 THEN 1
      WHEN summary <= 40000 THEN 2
      WHEN summary <= 60000 THEN 3
      WHEN summary <= 80000 THEN 4
      WHEN summary <= 100000 THEN 5
      ELSE 6
    END AS range_order,
    purchase_range,
    email_id
  FROM purchase_ranges
) ordered_ranges
GROUP BY purchase_range, range_order
ORDER BY range_order;

