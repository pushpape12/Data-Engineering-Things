# Data quality and contracts: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Schema contract
2. Grain and reconciliation
3. Quality gates and quarantine

## 1. Schema contract

### Understand it

A data contract describes structure and meaning: names, types, nullability, keys, ranges, units and version compatibility. A parseable record can still violate the business contract. Define what is rejected versus tolerated.

### Practical example

```json
{"order_id":1,"customer_id":101,"amount_cents":-50,"event_id":"e5","updated_at":"2026-10-01T10:04:00Z"}
```

**Expected result and reasoning:** Every field is present and structurally parseable, but the nonnegative-amount rule fails. Syntax validation alone would accept bad business data.

### Interview question

**Schema validation or business validation: which is enough?**

Both are needed. Validate structure at ingestion and business rules at the appropriate layer, preserving source coordinates and a repair path. State how schema evolution is handled.

**Common mistake:** Casting bad numeric strings to NULL and silently dropping them later.

**Try it yourself:** Specify a schema migration for changing currency from one fixed currency to multiple currencies.

## 2. Grain and reconciliation

### Understand it

Data quality needs more than uniqueness. A dataset missing half its orders can still have perfectly unique keys. Reconcile counts, totals and source manifests at compatible grains and intervals.

### Practical example

```bash
python python/etl.py
python data-quality/check.py
```

**Expected result and reasoning:** The shared fixture yields 3 current orders and 700 cents, from 5 valid input rows and 1 reject. These numbers refer to different grains intentionally.

### Interview question

**What controls would you use on a financial pipeline?**

Verify key uniqueness, null/range rules, interval completeness, source-to-target control totals and consistent units/currency. Investigate reconciliation differences without forcing totals to match by deleting data.

**Common mistake:** Comparing raw event count directly to current-order count as if they must match.

**Try it yourself:** Design control totals for insert/update/delete CDC, not only inserts.

## 3. Quality gates and quarantine

### Understand it

Choose whether a failed rule blocks all publication or quarantines individual rows within a reject budget. Retain enough evidence for remediation while controlling sensitive payload access and retention. Replays need the same identity rules as normal ingestion.

### Practical example

```text
6 records -> 5 accepted, 1 rejected
accepted -> deterministic current state -> reconcile -> publish
reject -> source coordinates + reason + repair owner
```

**Expected result and reasoning:** A successful pipeline can report a controlled reject, but it must not disguise an unbounded reject spike. The bundled lab reports metadata rather than storing a durable quarantine.

### Interview question

**When should a data issue fail the entire job?**

When integrity/completeness requirements cannot be met, a critical schema changes or the reject threshold is exceeded. Row isolation is appropriate only when the agreed contract permits partial acceptance.

**Common mistake:** Equating job SUCCESS with all records accepted.

**Try it yourself:** Define alert and remediation ownership for a 10% reject rate.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.
