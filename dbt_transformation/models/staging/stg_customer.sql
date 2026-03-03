with customers as (

    select
        id as customer_id,
        email,
        gender,
        currentaddressid
    from {{ source('raw_data', 'customer') }}

),

addresses as (

    select
        id as address_id,
        city,
    from {{ source('raw_data', 'address') }}

)

select
    c.customer_id,
    c.email,
    c.gender,
    a.city,
from customers c
left join addresses a
    on c.currentaddressid = a.address_id

-- select id, email, gender
-- from {{ source("raw_data", "customer") }}