-- ===========================================
-- GET ACC INFO
-- ===========================================
DROP TABLE IF EXISTS cpas_splitting;
CREATE TABLE IF NOT EXISTS cpas_splitting as
    (
with acc_shopee_managed AS (
SELECT
    distinct account_id
    -- , try_cast(shopid as bigint) as shop_id
FROM  dev_vnbi_mkt.acc_x_shop_id_line
WHERE true 
    and managed_by = 'Shopee managed'
) 

, acc_brand_managed as (
SELECT
      distinct account_id
    , count(distinct try_cast(shop_id as bigint)) as no_shop_id
FROM  dev_vnbi_mkt.acc_x_shop_id_line
WHERE true 
    and managed_by = 'Brand managed'
group by 1
)

, acc_x_managed AS (
SELECT
    distinct account_id, managed_by
    -- , try_cast(shopid as bigint) as shop_id
FROM  dev_vnbi_mkt.acc_x_shop_id_line
)

, acc_brand_managed__mapping as (
SELECT distinct account_id
FROM acc_brand_managed
WHERE true 
    and no_shop_id > 1
)

, acc_brand_managed__get_shop_id as (
SELECT 
  distinct a.account_id
, try_cast(shop_id as bigint) as shop_id
FROM dev_vnbi_mkt.acc_x_shop_id_line a 
left join acc_brand_managed__mapping b on a.account_id = b.account_id
left join acc_brand_managed c on a.account_id = c.account_id
WHERE true 
    and c.no_shop_id > 1
    and b.account_id is not null
)

, acc_brand_managed__no_mapping as (
SELECT
    distinct a.account_id, try_cast(b.shop_id as bigint) as shop_id

FROM acc_brand_managed a 
left join dev_vnbi_mkt.acc_x_shop_id_line b on a.account_id = b.account_id
WHERE true 
    and a.no_shop_id = 1
)


, full_acc_mapped as (
SELECT distinct account_id
FROM  dev_vnbi_mkt.acc_x_shop_id_line
WHERE true 
)


-- ===========================================
-- MAX GRASS_DATE
-- ===========================================
, get_max_grass_date as (
select min(max_grass_date) as max_grass_date
from (
            select 
                max(date(CAST(date_start AS timestamp))) as max_grass_date
                , 'ad level' as tablez 
            from regma_general.fb_cpas_full_ad_level_vn 
            group by 2
    union all   
            select 
            max(date(CAST(date_start AS timestamp))) as max_grass_date
            , 'full' as tablez 
            from regma_general.fb_cpas_full_vn 
            group by 2
    )
)

-- ===========================================
-- CALCULATE CONTRITBUTION
-- ===========================================

, contribution as (
    WITH ms_principal AS (
        SELECT distinct  try_cast(shop_id as bigint) shop_id
                        , account_id
                        -- , array_join(array_distinct(array_agg(account_id)), ', ') account_id
        FROM acc_x_shop_id_line
        )

        , traffic__by_ads_level as (
        SELECT
                date_trunc('month', grass_date) as grass_month
                , case when b.shop_id is not null then account_id else concat('ads-level',cast(b.shop_id as varchar)) end as account_id__mapping
                , sum(cast(visits as double)) visits
                , sum(gmv_usd) gmv_usd

        FROM offsite_shopee a
        left join ms_principal b on a.shop_id = b.shop_id 
        where true 
            and a.grass_date >= date'2021-01-01'
            and b.shop_id is not null
        group by 1,2
        )

        , traffic__by_shop_level as (
        SELECT
                date_trunc('month', grass_date) as grass_month
                , case when b.shop_id is not null then account_id else concat('ads-level',cast(b.shop_id as varchar)) end as account_id__mapping
                , b.account_id
                , a.shop_id
                , sum(cast(visits as double)) visits
                , sum(gmv_usd) gmv_usd

        FROM offsite_shopee a
        left join ms_principal b on a.shop_id = b.shop_id 
        where true 
            and a.grass_date >= date'2021-01-01'
            and b.shop_id is not null
            -- and date_trunc('month', grass_date) = date'2022-01-01'
        group by 1,2,3,4
        )

        select 
                      a.grass_month
                    -- , a.account_id__mapping
                    , a.account_id
                    , a.shop_id 
                    -- , a.visits 
                    -- , a.gmv_usd 
                    -- , b.visits as visit_ads_act_level 
                    -- , b.gmv_usd as gmv_usd_act_level
                    , if(is_nan(a.visits/b.visits), null, a.visits/b.visits) as contribution_by_visits
                    , if(is_nan(a.gmv_usd/b.gmv_usd), null, a.gmv_usd/b.gmv_usd) as contribution_by_gmv
        from traffic__by_shop_level a 
        left join traffic__by_ads_level b on a.grass_month = b.grass_month and a.account_id__mapping = b.account_id__mapping
)


-- ===========================================
-- CALCULATE CPAS DATA BY ADS LEVEL
-- ===========================================

, cpas_data__campaign_level as (
    with ex AS (
    SELECT DISTINCT
                grass_date
                , exchange_rate
                , currency
                , grass_region
    FROM mp_order.dim_exchange_rate__reg_s0_live
    WHERE (true AND (grass_date >= date '2021-01-01'))
    )

    , a AS (
    SELECT DISTINCT
                        a.account_id
                    , coalesce(
                        try_cast(regexp_extract(regexp_extract(lower(campaign_name), 's\d+_ss'), '\d+') as bigint),
                        try_cast(regexp_extract(regexp_extract(lower(campaign_name), 'p\d+_ss'), '\d+') as bigint)
                    ) as shop_id
                    , account_currency
                    , date(CAST(date_start AS timestamp)) grass_date

                    , "sum"(spend_usd) spend_usd
                    , "sum"((omni_purchase_value_7dc + omni_purchase_value_1dv)) gmv_value
                    , "sum"(outbound_clicks) outbound_click
                    , "sum"(impressions) impression
                    , "sum"(clicks) click
                    , "sum"((purchase_7dc + purchase_1dv)) orders
    FROM regma_general.fb_cpas_full_ad_level_vn a
    cross join get_max_grass_date
    WHERE true 
        AND date(CAST(date_start AS timestamp)) >= date '2021-01-01'
        and date(CAST(date_start AS timestamp)) <= max_grass_date
    GROUP BY 1,2,3,4
    )

    , b AS (
    SELECT DISTINCT
                    a.account_id
                    , a.shop_id
                    , account_currency
                    , a.grass_date
                    , spend_usd
                    , (CASE WHEN (a.account_currency = 'USD') THEN gmv_value ELSE (gmv_value / exchange_rate) END) gmv_usd
                    , outbound_click
                    , impression
                    , click
                    , orders
    FROM a
    LEFT JOIN ex ON ((a.grass_date = ex.grass_date) AND (a.account_currency = ex.currency))
    ) 

    SELECT DISTINCT
                  account_id
                , shop_id
                , date_trunc('month' , grass_date) as grass_month
                , grass_date
                , 'regma_general.fb_cpas_full_ad_level_vn' as table_source

                , "sum"(spend_usd) spend_usd
                , "sum"(gmv_usd) gmv_usd
                , "sum"(outbound_click) outbound_click
                , "sum"(impression) impression 
                , "sum"(orders) orders
                , "sum"(click) click 
                
    FROM b
    GROUP BY 1,2,3,4,5
    HAVING sum(spend_usd) > 0
)

, cpas_data__full as (
    with ex AS (
        SELECT DISTINCT
                    grass_date
                    , exchange_rate
                    , currency
                    , grass_region
        FROM mp_order.dim_exchange_rate__reg_s0_live
        WHERE (true AND (grass_date >= date '2021-01-01'))
        )

        , a AS (
        SELECT DISTINCT
                            a.account_id
                        , account_currency
                        , date(CAST(date_start AS timestamp)) grass_date
                        -- , campaign_name

                        , "sum"(spend_usd) spend_usd
                        , "sum"((omni_purchase_value_7dc + omni_purchase_value_1dv)) gmv_value
                        , "sum"(outbound_clicks) outbound_click
                        , "sum"(impressions) impression
                        , "sum"(clicks) click
                        , "sum"((purchase_7dc + purchase_1dv)) orders
        FROM regma_general.fb_cpas_full_vn a
        cross join get_max_grass_date
        WHERE true 
            AND date(CAST(date_start AS timestamp)) >= date '2021-01-01'
            and date(CAST(date_start AS timestamp)) <= max_grass_date
            -- AND (country = 'VN'))
        GROUP BY 1,2,3
        )

        , b AS (
        SELECT DISTINCT
                        a.account_id
                        , account_currency
                        , a.grass_date
                        -- , campaign_name
                        , spend_usd
                        , (CASE WHEN (a.account_currency = 'USD') THEN gmv_value ELSE (gmv_value / exchange_rate) END) gmv_usd
                        , outbound_click
                        , impression
                        , click
                        , orders
        FROM a
        LEFT JOIN ex ON ((a.grass_date = ex.grass_date) AND (a.account_currency = ex.currency))
        )
        
        SELECT DISTINCT
                      date_trunc('month' , grass_date) as grass_month
                    , grass_date
                    , account_id
                    , 'regma_general.fb_cpas_full_vn' as table_source

                    , "sum"(spend_usd) spend_usd
                    , "sum"(gmv_usd) gmv_usd
                    , "sum"(outbound_click) outbound_click
                    , "sum"(impression) impression 
                    , "sum"(orders) orders
                    , "sum"(click) click 
                    
        FROM b
        GROUP BY 1,2,3,4
        HAVING ("sum"(spend_usd) > 0)
)

-- ===========================================
-- GET FINAL RESULT BY SOURCE
-- ===========================================

, final_result__acc_shopee_managed__split_by_campaign_name as (
    SELECT DISTINCT
                  a.account_id
                , shop_id
                , grass_month
                , grass_date
                , 'Shopee managed - Split by campaign name' as type

                , "sum"(spend_usd) spend_usd
                , "sum"(gmv_usd) gmv_usd
                , "sum"(outbound_click) outbound_click
                , "sum"(impression) impression 
                , "sum"(orders) orders
                , "sum"(click) click 
                
    FROM cpas_data__campaign_level a 
    left join acc_shopee_managed b on a.account_id = b.account_id
    where b.account_id is not null
    GROUP BY 1,2,3,4,5
)

, final_result__acc_brand_managed_no_mapping__split_by_campaign_name as (
    SELECT DISTINCT
                  a.account_id
                , b.shop_id
                , a.grass_month
                , a.grass_date
                , 'Brand managed - 1 ads_account 1 shop_id' as type

                , "sum"(spend_usd) spend_usd
                , "sum"(gmv_usd) gmv_usd
                , "sum"(outbound_click) outbound_click
                , "sum"(impression) impression 
                , "sum"(orders) orders
                , "sum"(click) click 
                
    FROM cpas_data__full a 
    left join acc_brand_managed__no_mapping b on a.account_id = b.account_id
    where b.account_id is not null
    GROUP BY 1,2,3,4,5
)

, final_result__acc_brand_managed_mapping__split_by_contribution as (
    with cpas_brand_managed as (
        select 
                  a.account_id
                , grass_month
                , grass_date

                , sum(spend_usd) spend_usd
                , sum(gmv_usd) gmv_usd
                , sum(outbound_click) outbound_click
                , sum(impression) impression 
                , sum(orders) orders
                , sum(click) click 

        from cpas_data__full a 
        left join acc_brand_managed__mapping b on a.account_id = b.account_id
        where b.account_id is not null 
        group by 1,2,3
    )

    select 
              a.account_id 
            , b.shop_id
            , a.grass_month
            , a.grass_date
            , 'Brand managed - Split by visit contribution' as type

            , spend_usd * contribution_by_visits as spend_usd
            , gmv_usd * contribution_by_visits  as gmv_usd
            , outbound_click * contribution_by_visits  as outbound_click
            , impression * contribution_by_visits  as impression
            , orders * contribution_by_visits  as orders
            , click * contribution_by_visits  as click

    from cpas_brand_managed a 
    left join contribution b on a.account_id = b.account_id and a.grass_month = b.grass_month
    where b.account_id is not null
)

, final_result__acc_brand_managed_no_map_bp as (
    with before_bp_source as (
        select 
                  a.account_id
                , grass_month
                , grass_date

                , sum(spend_usd) spend_usd
                , sum(gmv_usd) gmv_usd
                , sum(outbound_click) outbound_click
                , sum(impression) impression 
                , sum(orders) orders
                , sum(click) click 

        from cpas_data__full a 
        left join acc_brand_managed__mapping b on a.account_id = b.account_id
        where b.account_id is not null 
        group by 1,2,3
    )

    , get_account_id__missing_by_date as (
        select distinct a.grass_date, a.account_id
        from before_bp_source a 
        left join final_result__acc_brand_managed_mapping__split_by_contribution b 
            on a.account_id = b.account_id 
            and a.grass_date = b.grass_date
        where b.account_id is null
    )

    select                   
                a.account_id 
            , d.shop_id
            , a.grass_month
            , a.grass_date
            , 'Brand managed - Split by total shop_id' as type

            , spend_usd/no_shop_id as spend_usd
            , gmv_usd/no_shop_id as gmv_usd
            , outbound_click/no_shop_id as outbound_click
            , impression/no_shop_id as impression 
            , orders/no_shop_id as orders
            , click/no_shop_id as click 

    from before_bp_source a 
    left join get_account_id__missing_by_date b on a.account_id = b.account_id and a.grass_date = b.grass_date -- GET MISSING BY DATE
    left join acc_brand_managed c on a.account_id = c.account_id -- GET NO SHOP_ID IN ACCOUNT_ID
    left join acc_brand_managed__get_shop_id d on a.account_id = d.account_id -- GET SHOP_ID IN ACCOUNT
    where b.account_id is not null -- FILTER DAILY MISSING DATA ONLY
)

, final_result__no_map as (
    SELECT DISTINCT
                  a.account_id
                , null as shop_id
                , date_trunc('month' , grass_date) as grass_month
                , grass_date
                , 'No mapping' as type

                , "sum"(spend_usd) spend_usd
                , "sum"(gmv_usd) gmv_usd
                , "sum"(outbound_click) outbound_click
                , "sum"(impression) impression 
                , "sum"(orders) orders
                , "sum"(click) click 
                
    FROM cpas_data__full a
    left join full_acc_mapped b on a.account_id = b.account_id
    where b.account_id is null 
    GROUP BY 1,2,3,4,5
)

-- ===========================================
-- GET SELLER INFO
-- ===========================================

, seller_info as (
    select distinct  
            shop_id
            , ado_segment
            , mall_segment
            , main_cat
            , function_detail
            , function
            , grass_month
            , case when function_detail in ('Mall','Retail','CB Mall') then 1 else 0 end as is_official_shop
            , case when function_detail like ('CB %') then 1 else 0 end as is_cb_shop                            
            , case  WHEN group_cat = 'EL&HA' THEN 'ELHA' 
                    WHEN group_cat = 'Cluster - Others' THEN 'Others'
                ELSE group_cat END clusters
    FROM vnbi_bd.dim_seller_type_1m_s0
)

-- ===========================================
-- GET FINAL DATA = FULL SOURCE + SELLER INFO
-- ===========================================

, data_ne as (
select a.*
            , case when mall_segment in ('Focus','ST','MT','LT') then mall_segment else ado_segment end as segment 
            , main_cat
            , function_detail
            , function
            , is_official_shop
            , is_cb_shop
            , clusters
            , c.managed_by
from (
            select * from final_result__acc_shopee_managed__split_by_campaign_name
union all   select * from final_result__acc_brand_managed_no_mapping__split_by_campaign_name
union all   select * from final_result__acc_brand_managed_mapping__split_by_contribution
union all   select * from final_result__acc_brand_managed_no_map_bp
union all   select * from final_result__no_map
) a 
left join seller_info b on a.shop_id = b.shop_id and a.grass_month = b.grass_month
left join acc_x_managed c on a.account_id = c.account_id
)

-- ===========================================
-- GET FINAL DATA AFTER MAPPING
-- ===========================================

select * --, max_grass_date
from data_ne
cross join get_max_grass_date
);

-- ===========================================
-- CODE CHEKC MISSING DATA
-- ===========================================

-- select distinct a.account_id, a.grass_month
-- from  (
--             select a.account_id, grass_month, sum(spend_usd) as spend_usd
--             from cpas_data a 
--             left join acc_brand_managed__mapping b on a.account_id = b.account_id
--             where b.account_id is not null 
--                 -- and a.grass_month = date'2022-01-01'
--             group by 1,2 
--          ) a 
-- left join  (
--         select grass_month, account_id, sum(spend_usd) spend_usd
--         from 
--         (
--                         select * from final_result__acc_brand_managed_mapping__split_by_contribution
--             union all   select * from final_result__acc_brand_managed_no_map_bp
--         )
--         -- where grass_month = date'2022-01-01'
--         group by 1,2
--         ) b
--     on a.account_id = b.account_id and a.grass_month = b.grass_month
-- where b.account_id is null 

