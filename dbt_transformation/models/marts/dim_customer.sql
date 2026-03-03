
with customers as (

    select *
    from {{ ref('stg_customer') }}

),

orders as (

    select *
    from {{ ref('stg_order') }}

),

customer_orders as (

    select
        c.customer_id,
        c.email,
        c.gender,
        c.city,

        min(o.order_timestamp) as first_order_date,
        max(o.order_timestamp) as most_recent_order_date,
        count(o.order_id) as number_of_orders

    from customers c
    left join orders o
        on c.customer_id = o.customer_id

    group by
        c.customer_id,
        c.email,
        c.gender,
        c.city
)

select *
from customer_orders
