select
    id as order_id,
    customer as customer_id,
    shippingaddressid as shipping_address_id,

    TIMESTAMP_MICROS(CAST(ordertimestamp / 1000 AS INT64)) as order_timestamp,

    CAST(total as NUMERIC) as total_amount,
    CAST(shippingcost as NUMERIC) as shipping_cost,

    TIMESTAMP_MICROS(CAST(created / 1000 AS INT64)) as created_at,
    TIMESTAMP_MICROS(CAST(updated / 1000 AS INT64)) as updated_at

from {{ source('raw_data', 'order') }}
