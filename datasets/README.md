# Synthetic order events

`orders.csv` contains six synthetic rows, including a duplicate delivery, a newer
version of order 1 and an invalid negative amount. No customer data is real.

| Field | Contract |
|---|---|
| order_id | Positive integer; business key |
| customer_id | Positive integer |
| amount_cents | Nonnegative integer; fixed-point currency in cents |
| updated_at | UTC timestamp in `YYYY-MM-DDTHH:MM:SSZ` format |
| event_id | Nonempty event identifier; lexical tie-breaker for equal timestamps |

For this fixture, deduplication after validation leaves three current orders:
`(1,101,150)`, `(2,102,250)`, `(3,101,300)`. Total: **700 cents**.
Five rows are valid, one is rejected. An identical replay must leave the same state.

Lexical event IDs provide a deterministic tie-breaker for this lab, not a universal
source ordering guarantee. Production CDC should use the source's sequence/LSN.
