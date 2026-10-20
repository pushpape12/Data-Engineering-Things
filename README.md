# Data Engineering Things

A practical data engineering learning repository: technology guides, worked topic
examples and a runnable pipeline that handles duplicates, stale events and rejects.
All example data is synthetic. Start with concepts, then choose tools for a problem.

## Preparing for an interview?

Start with the **[interview revision hub](INTERVIEW-PREP.md)**. It links **92 detailed topics across 23 technology/skill areas**, plus a **[six-question SQL coding workbook](sql/INTERVIEW-EXERCISES.md)**. Each topic explains the concept, gives a worked example and expected result, and includes a question/answer, common mistake and practice variation.

## Start in five minutes

Requires Python 3.11+ with sqlite3. Run from the repository root; no account or pip
installation is needed for this path.

```bash
python python/etl.py
python python/etl.py
python sql/run.py
python kafka/replay.py
python data-quality/check.py
python -m unittest discover -s tests -v
```

Expected current order state: **3 orders, 700 cents**, even after replay. Six source
rows contain an update, a duplicate delivery and an invalid negative amount.
See the [dataset contract](datasets/README.md) and [end-to-end project](projects/local-orders/README.md).

## Technology library

Each guide includes topic explanations, worked examples, prerequisites, expected
results and official references. Code blocks are either runnable in the listed lab
or explicitly marked as configuration/design templates. Optional runtimes are not
required by the quickstart.

| Technology or skill | What you learn |
|---|---|
| [Python for data pipelines](python/README.md) | Build small, explicit transformations with validation, deterministic ordering and retry-safe writes. |
| [SQL](sql/README.md) | Learn relational transformations before scaling to distributed engines. SQL dialects differ; this lab uses SQLite. |
| [Data engineering foundations](fundamentals/README.md) | Design pipelines around explicit grain, source ordering, data contracts and recoverability. |
| [Snowflake](snowflake/README.md) | Practice warehouse SQL, loading, semi-structured data, incremental state and operational controls. |
| [Apache Spark and PySpark](pyspark/README.md) | Use distributed DataFrames when data volume and shuffle work justify a cluster. Start with explicit schemas and built-in expressions. |
| [Databricks and Delta Lake](databricks/README.md) | Use Delta transactions with layered data products; distinguish Databricks platform features from open-source Spark. |
| [AWS data engineering](aws/README.md) | Compose object storage, catalog, compute and query services around an explicit data contract. |
| [Azure data engineering](azure/README.md) | Understand how ADLS storage, orchestration and analytics services fit together. |
| [Google Cloud data engineering](gcp/README.md) | Combine GCS landing data, BigQuery warehouse models and orchestration with source-aware replay. |
| [Apache Airflow](airflow/README.md) | Orchestrate dependencies and recovery; keep heavy data processing outside the scheduler. |
| [dbt](dbt/README.md) | Express warehouse transformations as versioned models with dependencies and data assertions. |
| [Apache Kafka and streaming](kafka/README.md) | Reason about keys, partitions, offsets and durable side effects before building a live consumer. |
| [Apache Iceberg and open table formats](iceberg/README.md) | Distinguish a columnar file from a transactional table whose metadata manages snapshots and schema changes. |
| [PostgreSQL](postgresql/README.md) | Practice transactional upserts, keys and query plans before using a database as a pipeline control plane. |
| [DuckDB](duckdb/README.md) | Run analytical SQL locally over files without operating a database server. |
| [Docker](docker/README.md) | Package a reproducible pipeline runtime while keeping configuration and data separate from the image. |
| [Terraform](terraform/README.md) | Model infrastructure inputs and review plans before any resource change. |
| [Data quality and contracts](data-quality/README.md) | Validate structure, business meaning and publication readiness separately. |
| [Pipeline observability](observability/README.md) | Track whether correct data arrived on time, not only whether a process exited successfully. |
| [Security and governance](security/README.md) | Separate read, transform, publish and administration privileges in data systems. |
| [pandas](pandas/README.md) | Transform in-memory datasets with explicit dtypes; switch to out-of-core or distributed execution when memory becomes limiting. |
| [File formats and data layout](file-formats/README.md) | Choose serialization and physical layout based on access patterns, schema stability and interoperability. |
| [Git and CI/CD for data projects](ci-cd/README.md) | Review transformation changes together with contracts and replay behavior before deployment. |
| [End-to-end project](projects/local-orders/README.md) | Connect ingestion, contracts, deduplication, transactions and recovery. |

## How to use this repository

- Follow the [learning path](LEARNING-PATH.md) for an ordered curriculum.
- Check [validation status](VALIDATION.md) before treating a snippet as runtime-tested.
- Run cloud examples only in an authorized sandbox; they can consume paid resources.
- Keep credentials in approved secret stores or secure environment configuration.
- Read each engine's prerequisites: SQL dialects and source ordering rules differ.

This is a substantial foundation, not an exhaustive encyclopedia of every product
or topic. Each included topic has a worked example; additional ecosystem modules
are identified separately in the learning path. No employer code or private data
is included. No license is added without the repository owner's choice.
