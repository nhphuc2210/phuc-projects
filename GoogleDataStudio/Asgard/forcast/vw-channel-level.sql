
create or replace view project_forecast_macro.channel_level as (
with channel_level as (
  with actual_data as (
    select 
    year
    , month
    , channel
    , 'Real' as Tipo_Dato
    , sum(sale_amount_MM) as sale_amount_MM
    from project_forecast_macro.ventas_por_familia_canal
    group by  1,2,3,4
  )

  , Pesimista as (
    -- Forecast_p5 = Pesimista
    select year	
    , month	
    , canal	as channel
    , 'Pesimista' as Tipo_Dato
    , sum(Forecast_p5) as sale_amount_MM
    from project_forecast_macro.forecasts_canales
    group by 1,2,3,4
  )

  , Optimista as (
    -- Forecast_p95 = Optimista
    select year	
    , month	
    , canal	as channel
    , 'Optimista' as Tipo_Dato
    , sum(Forecast_p95) as sale_amount_MM
    from project_forecast_macro.forecasts_canales
    group by 1,2,3,4
  )

  , Promedio as (
    -- Forecast_Promedio = Promedio
    select year	
    , month	
    , canal	as channel
    , 'Promedio' as Tipo_Dato
    , sum(Forecast_Promedio) as sale_amount_MM
    from project_forecast_macro.forecasts_canales
    group by 1,2,3,4
  )

  select 
    year	
    , month	
    , channel
    , Tipo_Dato
    , sale_amount_MM as sale_amount_MM_local
  , sale_amount_MM/972.75 as sale_amount_MM_usd
  from (
            select * from actual_data
  union all select * from Pesimista
  union all select * from Optimista
  union all select * from Promedio
  )
)

select * from channel_level
)




