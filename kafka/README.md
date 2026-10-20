# Apache Kafka and streaming

Reason about keys, partitions, offsets and durable side effects before building a live consumer.

[Back to repository index](../README.md)

## Interview revision

Read the [detailed topic explanations, worked examples and interview answers](INTERVIEW.md). Every original topic in this guide is expanded there.

## Prerequisites and lab

Run `python kafka/replay.py` with standard Python. This is a local semantics simulation, not a broker integration test. For a real broker, follow the official quickstart in an isolated environment.

## Topics with worked examples

### Keys and ordering

Ordering is per partition. Key related events consistently; a topic-wide global order is not automatic.

```text
key=order_id -> partition -> ordered offset sequence
partition 0: offsets 0,1,2
partition 1: offsets 0,1
```

**Check:** An offset is meaningful together with topic and partition.

### Consumer groups and commits

Consumers in a group share partitions. Commit after processing; a crash after sink commit can replay the record.

```bash
python kafka/replay.py
```

**Check:** Naive accumulation totals 800 cents; idempotent event-key writes total 400.

### Exactly-once boundaries

Kafka transactions can atomically coordinate supported Kafka reads/writes. An arbitrary external database is outside that boundary unless explicitly integrated.

```text
sink transaction commits -> consumer crashes -> offset not committed
restart -> event delivered again -> unique event key prevents double insert
```

**Check:** Use durable sink transactions, not the in-memory dictionary from this teaching simulation.

### Schema evolution and poison events

Version event contracts and quarantine invalid messages with source coordinates. Do not log sensitive payloads by default.

```json
{"schema_version":1,"event_id":"e1","order_id":1,"amount_cents":150}
```

**Check:** Consumers validate required fields and policy for unknown fields before side effects.

## Official references

- https://kafka.apache.org/quickstart/
- https://kafka.apache.org/documentation/

Documentation checked: 2026-10-20. Examples are educational; cloud and engine-specific labs require their listed environment. See [validation status](../VALIDATION.md).
