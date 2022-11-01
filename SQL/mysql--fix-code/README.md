# **Waiting for final code**

## **ORIGINAL CODE** 

```sql

WITH user_info as (
SELECT 
distinct 
        
      order_report.order_time
    , customer_id as users
    ,   b.is_ula_companion as companion
    ,   case when date((order_report.order_time),'Asia/Jakarta') > date(min(order_report.order_time),'Asia/Jakarta') 
            then "Repeat User" 
            else "New User" end as user_type

FROM `ula-backend.order.order_report` as order_report
LEFT JOIN `ula-backend.raw.user` as b ON order_report.customer_id = b.id
group by 1,2,order_report.order_time
)



, my_raw_data as (
    SELECT distinct
    date(order_item_v2.created_at,'Asia/Jakarta') as order_date_jkt
    , user_info.user_type
    , user_info.companion

    from raw.order_items_additional_info
    left join raw.order_item_v2 -- GET CREATED DATE
        on order_item_v2.id = order_items_additional_info.order_item_id      
    left join `ula-backend.order.order_report` as order_report -- GET CUSTOMER_ID
        on order_report.order_id = order_item_v2.order_id
        on date((order_report.order_time),'Asia/Jakarta') = date(order_item_v2.created_at,'Asia/Jakarta')
    left join user_info -- GET USER_TYPE
        on order_report.customer_id = user_info.users 
        and user_info.order_time = date((order_report.order_time),'Asia/Jakarta')
    )



SELECT
  group_date
, companion

, count(distinct users) as total_users
, count(distinct case when user_type = 'Repeat User' then users end) as repeat_users,
, count(distinct case when user_type = 'New User' then users end) as new_user 


FROM my_raw_data temp

where true  
group by 1,2
order by 1 desc 
```