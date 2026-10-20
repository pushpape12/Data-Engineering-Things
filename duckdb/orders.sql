-- DuckDB CLI: duckdb < duckdb/orders.sql (run from repository root).
CREATE TEMP VIEW raw AS SELECT * FROM read_csv('datasets/orders.csv',header=true,
 columns={'order_id':'BIGINT','customer_id':'BIGINT','amount_cents':'BIGINT','updated_at':'VARCHAR','event_id':'VARCHAR'});
CREATE TEMP VIEW current_orders AS
 SELECT * EXCLUDE(rn) FROM (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY updated_at DESC,event_id DESC) rn
 FROM raw WHERE amount_cents>=0) WHERE rn=1;
SELECT customer_id,SUM(amount_cents) revenue_cents FROM current_orders GROUP BY customer_id ORDER BY customer_id;
-- Expected (101,450),(102,250).
