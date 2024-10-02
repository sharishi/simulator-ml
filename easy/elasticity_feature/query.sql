SELECT sku, dates, price, COUNT(sku) AS qty
FROM transactions
GROUP BY sku, dates, price