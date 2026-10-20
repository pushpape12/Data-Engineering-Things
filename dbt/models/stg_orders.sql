-- Adapter-neutral basics; equal version conflicts must be checked upstream.
with ranked as (
 select *, row_number() over (
 partition by order_id order by updated_at desc,event_id desc) as rn
 from {{ ref('raw_orders') }} where amount_cents>=0
)
select order_id,customer_id,amount_cents,updated_at,event_id from ranked where rn=1
