WITH raw_data AS (
    SELECT
        tag,
        unixtime,
        JSONExtractString(data, 'order_id') as order_id,
        JSONExtractFloat(data, 'price') as price,
        JSONExtractFloat(data, 'freight_value') as freight_value
    FROM `olist`.`ingestion`
    WHERE tag = 'olist_order_items_dataset.csv'
)

SELECT
    order_id,
    price,
    freight_value,
    unixtime as ingested_at
FROM raw_data