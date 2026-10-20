select customer_id,sum(amount_cents) as revenue_cents
from {{ ref('stg_orders') }} group by customer_id
