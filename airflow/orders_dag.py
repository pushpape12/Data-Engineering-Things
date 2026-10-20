"""Airflow 3 TaskFlow example; tasks pass small metadata, not large datasets."""
from datetime import datetime, timezone, timedelta
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
     catchup=False, default_args={"retries": 2, "retry_delay": timedelta(minutes=1)},
     tags=["learning", "orders"])
def orders_learning():
    @task
    def extract_manifest():
        # Deterministic in-memory sample. Real tasks should use data_interval bounds.
        return [{"order_id": 1, "amount_cents": 150}, {"order_id": 2, "amount_cents": 250}]

    @task
    def validate(rows):
        if any(row["amount_cents"] < 0 for row in rows):
            raise ValueError("Negative order amount")
        return {"rows": len(rows), "total_cents": sum(row["amount_cents"] for row in rows)}

    @task
    def report(metrics):
        print(metrics)  # Expected rows=2, total_cents=400. No external write.

    report(validate(extract_manifest()))

orders_learning()
