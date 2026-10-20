# Azure data engineering: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. ADLS Gen2 and identities
2. Data Factory pipeline parameters
3. Watermarks and publication

## 1. ADLS Gen2 and identities

### Understand it

An identity authenticates the workload; authorization determines which storage paths it can read/write. Azure role assignments and filesystem ACLs serve different scopes. Managed identities avoid putting long-lived account keys in application code.

### Practical example

```text
workload managed identity -> required storage role/ACLs
landing container -> reader access
curated output path -> writer access
```

**Expected result and reasoning:** A landing reader should not automatically be able to delete all curated data. Check both storage permissions and the exact execution identity.

### Interview question

**A pipeline can list a container but cannot read one directory. Why?**

Inspect the identity used by the activity, applicable roles/conditions and directory traversal/file ACLs. Validate the specific path rather than replacing scoped access with an account key.

**Common mistake:** Testing as your personal user and assuming the pipeline has the same access.

**Try it yourself:** Define the minimum permissions for a transform that reads landing and writes curated.

## 2. Data Factory pipeline parameters

### Understand it

A pipeline orchestrates activities; linked services describe connections and datasets describe data locations/shape. Parameters make one pipeline reusable for a specific interval; mutable variables are not a substitute for independent per-run input.

### Practical example

```json
{"pipeline":"orders_daily","parameters":{"run_date":"2026-10-01","source_container":"landing","target_container":"curated"}}
```

**Expected result and reasoning:** This is an illustrative run configuration, not an ADF deployment payload. The same code can process different dates without editing its activities.

### Interview question

**How would you make a daily copy pipeline reusable?**

Parameterize the logical date, source path and destination; bind dataset expressions to pipeline parameters; control retries/concurrency and validate publication before recording progress.

**Common mistake:** Using current date inside every activity, which breaks historical reruns.

**Try it yourself:** Explain how two simultaneous date backfills avoid writing to the same output.

## 3. Watermarks and publication

### Understand it

Capture a bounded source interval, extract it, validate the destination and only then publish the new checkpoint. Replay overlap is useful for late updates but requires a stable merge key and source-order guard. Hard deletes need separate CDC or reconciliation.

### Practical example

```text
last_success=10:00
capture source_high=10:05
extract (10:00,10:05] plus defined overlap
merge -> reconcile -> save source_high
```

**Expected result and reasoning:** A failure before checkpoint advancement reprocesses the interval. A simple max timestamp can miss changes with equal timestamps unless tie rules/overlap are designed.

### Interview question

**What happens if the watermark advances before output succeeds?**

A restart may skip data that never reached the destination. Persist progress only after reliable output completion, or coordinate a recoverable two-phase publication protocol.

**Common mistake:** Using processing clock time instead of a captured source boundary.

**Try it yourself:** Handle a record modified at exactly the previous watermark timestamp.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.
