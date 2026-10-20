"""Simulate a consumer crash after sink commit but before offset commit."""
from collections import Counter
messages = [(0, "e1", 150), (1, "e2", 250)]
naive = Counter()
for _, event, amount in messages + messages:
    naive["revenue_cents"] += amount
sink = {}
for offset, event, amount in messages + messages:
    sink.setdefault(event, amount)
print({"naive_cents": naive["revenue_cents"], "idempotent_cents": sum(sink.values())})
if sum(sink.values()) != 400:
    raise RuntimeError("Replay changed logical total")
