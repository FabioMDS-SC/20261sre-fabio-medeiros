
  
    
    
    
        
         


        
  

  insert into `olist`.`fct_orders__dbt_backup`
        ("order_id", "customer_id", "order_status", "order_purchase_at", "order_date", "total_items_value", "total_freight_value", "total_order_value", "total_items")WITH orders AS (
    SELECT * FROM `olist`.`stg_orders`
),

items AS (
    SELECT 
        order_id,
        sum(price) as total_items_value,
        sum(freight_value) as total_freight_value,
        count(*) as total_items
    FROM `olist`.`stg_order_items`
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_at,
    toStartOfDay(o.order_purchase_at) as order_date,
    i.total_items_value,
    i.total_freight_value,
    i.total_items_value + i.total_freight_value as total_order_value,
    i.total_items
FROM orders o
LEFT JOIN items i ON o.order_id = i.order_id
  