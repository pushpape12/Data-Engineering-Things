-- BigQuery GoogleSQL. Replace YOUR_PROJECT and sandbox dataset; use a sandbox project.
CREATE TABLE `YOUR_PROJECT.sandbox.de_lab_orders` (
 order_id INT64, customer_id INT64, amount_cents INT64, order_date DATE
) PARTITION BY order_date CLUSTER BY customer_id
OPTIONS(require_partition_filter=TRUE);
INSERT INTO `YOUR_PROJECT.sandbox.de_lab_orders` VALUES
 (1,101,150,DATE '2026-10-01'),(2,102,250,DATE '2026-10-01');
SELECT customer_id,SUM(amount_cents) AS revenue_cents
FROM `YOUR_PROJECT.sandbox.de_lab_orders`
WHERE order_date=DATE '2026-10-01' GROUP BY customer_id;
-- Cleanup: DROP TABLE `YOUR_PROJECT.sandbox.de_lab_orders`;
