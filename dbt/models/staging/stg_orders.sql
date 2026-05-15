WITH raw_data AS (
    SELECT
        tag,
        unixtime,
        JSONExtractString(data, 'order_id') as order_id,
        JSONExtractString(data, 'customer_id') as customer_id,
        JSONExtractString(data, 'order_status') as order_status,
        JSONExtractString(data, 'order_purchase_timestamp') as order_purchase_timestamp
    FROM {{ source('clickhouse_ingestion', 'ingestion') }}
    WHERE tag = 'olist_orders_dataset.csv'
)

SELECT
    order_id,
    customer_id,
    order_status,
    parseDateTimeBestEffort(order_purchase_timestamp) as order_purchase_at,
    unixtime as ingested_at
FROM raw_data
