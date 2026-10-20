# Apache Airflow

Orchestrate dependencies and recovery; keep heavy data processing outside the scheduler.

[Back to repository index](../README.md)

## Prerequisites and lab

Airflow 3.x SDK example. Use an existing isolated Airflow environment; copy `orders_dag.py` into its dags folder and run `airflow dags test orders_learning 2026-10-02`. Not runtime-tested here.

## Topics with worked examples

### DAGs and TaskFlow

Decorated task calls define dependencies rather than executing work while parsing the DAG. Keep network reads out of top-level DAG code.

```python
report(validate(extract_manifest()))
```

**Check:** The example forms extract -> validate -> report.

### Retries and idempotency

Airflow can retry a task after its external write succeeded but before success was recorded. Use an idempotent sink.

```python
default_args={"retries":2,"retry_delay":timedelta(minutes=1)}
```

**Check:** Two retries do not provide exactly-once delivery.

### Scheduling and logical intervals

Use the scheduled data interval rather than machine time for reproducible daily partitions.

```python
from airflow.sdk import get_current_context
# Inside a task:
context = get_current_context()
start = context["data_interval_start"]
end = context["data_interval_end"]
```

**Check:** Read source event_time >= start and < end, plus an explicit late-event strategy.

### XComs and connections

Pass small metadata or storage URIs through XComs. Store credentials in configured Connections/secrets backends, not DAG source.

```text
Task A writes parquet -> returns {uri, checksum, row_count}
Task B reads the URI and validates checksum
```

**Check:** The bundled DAG uses only two tiny rows to demonstrate dependencies.

## Official references

- https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html
- https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).
