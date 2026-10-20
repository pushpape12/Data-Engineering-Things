from pathlib import Path
import pandas as pd
path = Path(__file__).resolve().parents[1] / "datasets/orders.csv"
df = pd.read_csv(path, dtype={"order_id":"int64", "customer_id":"int64", "amount_cents":"int64",
                              "updated_at":"string", "event_id":"string"})
valid = df.loc[df.amount_cents.ge(0) & df.order_id.gt(0) & df.customer_id.gt(0)]
current = valid.sort_values(["updated_at","event_id"]).drop_duplicates("order_id", keep="last")
result = current.groupby("customer_id")["amount_cents"].sum().sort_index()
if result.to_dict() != {101:450,102:250}:
    raise RuntimeError(f"Unexpected totals: {result}")
print(result.to_string())
