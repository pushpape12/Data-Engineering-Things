# Azure data engineering

Understand how ADLS storage, orchestration and analytics services fit together.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Architecture and configuration examples for an Azure sandbox; no resources created. Use ADF Studio or your approved deployment process for executable activities.

## Topics with worked examples

### ADLS Gen2 and identities

Use managed identity where supported. Distinguish storage RBAC from filesystem ACLs and check both on the intended path.

```text
abfss://landing@YOUR_ACCOUNT.dfs.core.windows.net/orders/ingest_date=2026-10-01/
```

**Check:** Use a dedicated sandbox container; do not embed account keys in notebooks.

### Data Factory pipeline parameters

A pipeline groups activities; linked services configure connections and datasets describe data. Parameterize dates instead of using today() inside backfills.

```json
{"name":"orders_daily","properties":{"parameters":{"run_date":{"type":"String","defaultValue":"2026-10-01"}},"activities":[]}}
```

**Check:** This is a parameter-only pipeline definition, not an executable copy job. Add authorized linked services, datasets and a Copy activity in ADF Studio.

### Watermarks and publication

Capture a source high watermark before extraction, replay a bounded overlap, and advance the checkpoint only after output succeeds. Timestamp watermarks alone cannot reliably capture hard deletes.

```text
last_success=10:00 -> read through source_high=10:05
merge source versions -> validate output -> persist source_high
```

**Check:** A failure before final commit must allow the same interval to be retried.

## Official references

- https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities
- https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).
