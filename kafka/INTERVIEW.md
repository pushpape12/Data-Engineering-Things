# Apache Kafka and streaming: interview study notes

[Technology guide and lab setup](README.md) · [Interview revision hub](../INTERVIEW-PREP.md)

Read the explanation, predict the example result, then answer the interview question aloud. Examples below are worked exercises; they have not been executed in this revision. Reuse the linked lab prerequisites. SQL dialects are identified explicitly. Production scenarios are hypothetical, not personal experience claims.

## Topic index

1. Keys and ordering
2. Consumer groups and commits
3. Exactly-once boundaries
4. Schema evolution and poison events

## 1. Keys and ordering

### Understand it

Kafka orders records within a partition, not across an entire topic. A key influences partition selection; related business events should use a consistent strategy. Adding partitions can change key placement for future records under some partitioners.

### Practical example

```text
topic orders, partition 0: offset 8 order=1,v1; offset 9 order=1,v2
topic orders, partition 1: offset 8 order=2,v1
```

**Expected result and reasoning:** Offset 8 on partition 0 has no ordering relationship to offset 8 on partition 1. Application versions still matter when integrating other sources.

### Interview question

**Can Kafka guarantee global ordering?**

Only within a partition. One partition can impose a single sequence but limits parallelism. For per-entity consistency, key related events appropriately and enforce source versions at the state sink.

**Common mistake:** Comparing bare offsets from different partitions.

**Try it yourself:** Explain the ordering considerations when increasing a topic's partition count.

## 2. Consumer groups and commits

### Understand it

Within a normal consumer group, partitions are assigned among active consumers. Extra consumers beyond available partitions cannot independently parallelize those assignments. A committed offset tells the group where to resume, not whether an arbitrary external side effect is correct.

### Practical example

```text
topic has 3 partitions; group has 5 consumers
up to 3 consumers receive normal partition assignments
sink write -> commit offset -> next record
```

**Expected result and reasoning:** Two consumers may have no assignments. If a consumer fails, reassignment may replay work after its last committed progress.

### Interview question

**What happens if you commit before processing?**

A crash can skip an unprocessed record. Commit after successful processing to avoid that loss window, but then handle duplicates from crashes between processing and offset commit.

**Common mistake:** Treating consumer lag as a direct measurement of business-data freshness.

**Try it yourself:** Describe what a rebalance does to in-flight external database work.

## 3. Exactly-once boundaries

### Understand it

State the boundary of any exactly-once claim. Supported Kafka transactions can coordinate Kafka-side effects and offsets, but an unrelated external database needs its own integration or idempotent pattern. Delivery, processing attempts and final business results differ.

### Practical example

```bash
python kafka/replay.py
```

**Expected result and reasoning:** The simulation prints naive_cents=800 and idempotent_cents=400. It deliberately repeats both events to show the commit/offset failure window.

### Interview question

**How would you write Kafka events to PostgreSQL safely?**

Use stable event IDs or source versions, a transactional sink and replay-safe upserts. Consider storing consumed source coordinates with sink state in the same transaction where feasible. Recover group offsets deliberately; do not claim universal atomicity.

**Common mistake:** Using an in-memory set as durable deduplication across restarts.

**Try it yourself:** Show how a unique event-ID table and business update can commit together.

## 4. Schema evolution and poison events

### Understand it

Consumers need a contract, compatibility rules and a policy for malformed or permanently unprocessable records. A dead-letter stream needs source coordinates, sanitized diagnostics and replay ownership; it must not become an unmonitored dumping ground.

### Practical example

```json
{"schema_version":2,"event_id":"e1","order_id":1,"amount_cents":150,"currency":"INR"}
```

**Expected result and reasoning:** An added field may be compatible if consumers tolerate it; changing amount_cents from integer to arbitrary text is a different contract change.

### Interview question

**Would you retry a malformed event forever?**

No. Classify permanent validation failures, quarantine with enough metadata for repair, advance processing only according to the agreed policy, and alert on reject thresholds. Retry transient service failures with bounds.

**Common mistake:** Discarding the source identity when sending an event to quarantine.

**Try it yourself:** Define how corrected poison events are replayed without double-applying old ones.

## Reference and validation

Use the official documentation links in the [technology guide](README.md). These notes extend that guide; they do not replace version-specific documentation. See [validation status](../VALIDATION.md) for the distinction between previously executed labs and new unexecuted worked exercises.
