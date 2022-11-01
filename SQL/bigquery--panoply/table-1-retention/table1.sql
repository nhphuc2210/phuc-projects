with register_table as (
  SELECT
      id
    , created_at
    , DATE(created_at) AS sign_up_date
  FROM `panoply.postgres_core_user`
  where true
    -- and id in (24320)
)

, tracking_table as (
select user_id, app_screen, created_at, date(created_at) as grass_date
from `panoply.postgres_tracking_eventtrackingmodel`
where true 
  and user_id is not null  
  and app_screen = 'home_screen'
)

select distinct
          grass_date
-- , DATE_ADD(grass_date, INTERVAL -2 DAY)

        , count(distinct user_id) as total_user
        , count(distinct case when b.sign_up_date >= a.grass_date then user_id end) as new_user
        , count(distinct user_id) - count(distinct case when b.sign_up_date >= a.grass_date then user_id end) as users_returning

        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -1 DAY) then user_id end) as d1
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -2 DAY) then user_id end) as d2
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -3 DAY) then user_id end) as d3
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -4 DAY) then user_id end) as d4
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -5 DAY) then user_id end) as d5
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -6 DAY) then user_id end) as d6
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -7 DAY) then user_id end) as d7
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -8 DAY) then user_id end) as d8
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -9 DAY) then user_id end) as d9
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -10 DAY) then user_id end) as d10
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -11 DAY) then user_id end) as d11
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -12 DAY) then user_id end) as d12
        , count(distinct case when sign_up_date = DATE_ADD(grass_date, INTERVAL -13 DAY) then user_id end) as d13
        
        , count(distinct case when sign_up_date between DATE_ADD(grass_date, INTERVAL -6 DAY) and date_add(grass_date, interval -1 day) and sign_up_date <> grass_date then user_id end) as w0
        , count(distinct case when sign_up_date between DATE_ADD(grass_date, INTERVAL -13 DAY) and date_add(grass_date, interval -7 day) and sign_up_date <> grass_date then user_id end) as w1
        , count(distinct case when sign_up_date between DATE_ADD(grass_date, INTERVAL -20 DAY) and date_add(grass_date, interval -14 day) and sign_up_date <> grass_date then user_id end) as w2
        , count(distinct case when sign_up_date between DATE_ADD(grass_date, INTERVAL -26 DAY) and date_add(grass_date, interval -21 day) and sign_up_date <> grass_date then user_id end) as w3
        , count(distinct case when sign_up_date < date_add(grass_date, interval -26 day) and sign_up_date <> grass_date then user_id end) as w4_

from tracking_table a 
left join register_table b on a.user_id = b.id 
where true 
  -- and a.create_date = b.create_date
  -- and user_id = 24320
group by 1
order by 1



