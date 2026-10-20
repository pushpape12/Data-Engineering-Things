-- Snowflake dialect. Run in a dedicated scratch database/schema.
-- Requires an active warehouse and CREATE TABLE/STREAM/TASK privileges.
-- Change the context below to an existing sandbox, never production.
-- USE DATABASE YOUR_SANDBOX_DB;
-- USE SCHEMA YOUR_SANDBOX_SCHEMA;
-- USE WAREHOUSE YOUR_SANDBOX_WH;
CREATE TEMP TABLE de_lab_events(order_id INT,customer_id INT,amount_cents INT,
 updated_at TIMESTAMP_NTZ,event_id VARCHAR);
INSERT INTO de_lab_events VALUES
 (1,101,100,'2026-10-01 10:00:00','e1'),
 (1,101,150,'2026-10-01 10:02:00','e3'),
 (2,102,250,'2026-10-01 10:01:00','e2'),
 (3,101,300,'2026-10-01 10:03:00','e4');
CREATE TEMP TABLE de_lab_orders LIKE de_lab_events;
MERGE INTO de_lab_orders t USING (
 SELECT * FROM de_lab_events QUALIFY ROW_NUMBER() OVER(
 PARTITION BY order_id ORDER BY updated_at DESC,event_id DESC)=1
) s ON t.order_id=s.order_id
WHEN MATCHED AND (s.updated_at>t.updated_at OR
 (s.updated_at=t.updated_at AND s.event_id>t.event_id)) THEN
 UPDATE SET customer_id=s.customer_id,amount_cents=s.amount_cents,
 updated_at=s.updated_at,event_id=s.event_id
WHEN NOT MATCHED THEN INSERT VALUES(s.order_id,s.customer_id,s.amount_cents,s.updated_at,s.event_id);
SELECT COUNT(*) AS orders,SUM(amount_cents) AS total_cents FROM de_lab_orders;
-- Expected 3,700. Rerun only MERGE to prove replay safety.
SELECT PARSE_JSON('{"items":[{"sku":"A","qty":2}]}') AS payload;
WITH docs AS (SELECT PARSE_JSON('{"items":[{"sku":"A","qty":2}]}') payload)
SELECT f.value:sku::VARCHAR sku,f.value:qty::INT qty
FROM docs,LATERAL FLATTEN(INPUT=>payload:items) f;
