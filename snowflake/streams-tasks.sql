-- Run separately in an existing sandbox schema. These are persistent lab objects.
-- CREATE without OR REPLACE prevents accidental loss of a stream offset on rerun.
CREATE TABLE de_lab_append_source(order_id INT,amount_cents INT);
CREATE TABLE de_lab_append_sink(order_id INT,amount_cents INT);
CREATE STREAM de_lab_append_stream ON TABLE de_lab_append_source APPEND_ONLY=TRUE;
INSERT INTO de_lab_append_source VALUES(1,150),(2,250);
SELECT * FROM de_lab_append_stream; -- Does NOT consume the stream.
INSERT INTO de_lab_append_sink SELECT order_id,amount_cents FROM de_lab_append_stream;
SELECT COUNT(*) FROM de_lab_append_stream; -- Expected 0 after committed INSERT.
-- Replace YOUR_SANDBOX_WH with an existing warehouse before running this statement.
CREATE TASK de_lab_append_task WAREHOUSE=YOUR_SANDBOX_WH SCHEDULE='5 MINUTE'
 WHEN SYSTEM$STREAM_HAS_DATA('de_lab_append_stream')
 AS INSERT INTO de_lab_append_sink SELECT order_id,amount_cents FROM de_lab_append_stream;
-- Task is created suspended. RESUME is deliberately not executed.
-- To clean up this lab after inspecting it:
-- DROP TASK de_lab_append_task;
-- DROP STREAM de_lab_append_stream;
-- DROP TABLE de_lab_append_sink;
-- DROP TABLE de_lab_append_source;
