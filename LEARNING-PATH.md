# Learning path

[Repository index](README.md)

| Stage | Study | Exercise and completion check |
|---|---|---|
| 1. Contracts and SQL | fundamentals, sql, file-formats | Explain why six events produce three current orders; reproduce the 700-cent total. |
| 2. Reliable Python | python, pandas, data-quality | Run the ETL twice; invalid rows remain excluded and totals do not grow. |
| 3. Storage and warehouses | postgresql, duckdb, snowflake | Compare constraints and guarded upserts; do not assume identical SQL dialects. |
| 4. Distributed compute | pyspark, databricks, iceberg | Reproduce latest-state deduplication, inspect a query plan and describe a snapshot. |
| 5. Cloud architecture | aws, azure, gcp | Map storage, catalog, processing and query responsibilities to each provider. |
| 6. Orchestration and models | airflow, dbt | Use data intervals, dependency graphs, model tests and explicit backfill rules. |
| 7. Streaming | kafka | Explain the crash window between sink commit and offset commit. |
| 8. Operations | docker, terraform, ci-cd, observability, security | Review a build/plan, run CI, and document failure recovery and access boundaries. |
| 9. Integration | projects/local-orders | Demonstrate replay, stale-event protection and atomic rollback. |

Study in this order, not by installing every tool at once. The local standard-library
project is the common baseline. Choose one cloud and warehouse for deeper labs.

## Broader ecosystem

This first edition covers a broad foundation, not every data engineering product.
Flink, Beam, Hadoop/Hive, Trino, Kubernetes, Debezium, MongoDB, Elasticsearch,
Power BI and platform-specific advanced topics are natural later modules.
Add a module only with explanation, a worked example, expected results and honest
validation status; a folder name alone is not a completed lesson.

## Interview mode

Use the [interview revision hub](INTERVIEW-PREP.md) to revise topic explanations and practise scenario answers. For coding preparation, attempt the [SQL workbook](sql/INTERVIEW-EXERCISES.md) before reading its expandable solutions. Every technology guide now links to its detailed INTERVIEW.md notes.
