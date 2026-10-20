# Validation status

[Repository index](README.md)

## Local checks

The following are executed before publication in the development environment:

- Python standard-library ETL on the shared fixture, then a replay.
- In-memory SQLite SQL exercise with expected customer totals.
- Kafka delivery-semantics simulation (not a broker integration).
- Read-only fixture quality check.
- Five unit tests: replay, late event, rollback, invalid timestamp and version conflict.
- pandas fixture transformation when pandas is available locally.
- Syntax compilation of Python examples, without importing optional runtimes.
- Markdown relative file-link resolution, YAML parsing and Git whitespace checks.

## Requires external runtime or account; not executed here

| Area | Required validation before production use |
|---|---|
| Snowflake | Execute both SQL labs in a scratch schema; verify permissions, stream consumption and task suspension. |
| Spark | Install a compatible Spark/Python/JDK combination; run orders.py and inspect query plans. |
| Databricks/Delta | Execute merge.sql in a scratch schema and replay its MERGE statement. |
| Airflow | Parse and test orders_learning in Airflow 3.x; use a deployment-specific metadata/backend configuration. |
| dbt | Install compatible dbt-core/dbt-duckdb, create a local profile, then seed/run/test. |
| PostgreSQL | Run upsert.sql with ON_ERROR_STOP in a sandbox database. |
| DuckDB/Parquet | Execute orders.sql with DuckDB CLI; install a Parquet engine for optional pandas output. |
| AWS/Azure/GCP | Resolve placeholders, authenticate with least privilege, verify schemas and estimate cost. |
| Iceberg | Configure a compatible catalog, extensions and runtime; execute against a disposable table. |
| Docker | Build and run the image; assess base-image digest and vulnerabilities. |
| Terraform | Run init/validate/plan; no provider or resources are declared. |
| GitHub Actions | Check the actual PR workflow result after push; local checks do not imply hosted CI success. |

Checked documentation date: 2026-10-20. Current documentation URLs can evolve;
use version-specific documentation when pinning a real deployment. Cloud templates
are educational starting points, not deploy-and-forget production systems.
