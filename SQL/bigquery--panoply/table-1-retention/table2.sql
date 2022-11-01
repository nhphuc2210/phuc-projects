with register_table as (
  SELECT
      id
    , created_at
    , DATE(created_at) AS sign_up_date
    , date(DATE_TRUNC(created_at, week(MONDAY))) as week_start
  FROM `panoply.postgres_core_user`
  where true
)


, tracking_table as (
select user_id, app_screen, created_at, date(created_at) as grass_date
from `panoply.postgres_tracking_eventtrackingmodel`
where true 
  and user_id is not null  
  and app_screen = 'home_screen'
)

select   
         week_start
        , sign_up_date

        , count(distinct case when a.sign_up_date = grass_date then id end) as total

        , count(distinct case when grass_date = date_add(sign_up_date, interval +1 day) then id end) as day1
        , count(distinct case when grass_date = date_add(sign_up_date, interval +2 day) then id end) as day2
        , count(distinct case when grass_date = date_add(sign_up_date, interval +3 day) then id end) as day3
        , count(distinct case when grass_date = date_add(sign_up_date, interval +4 day) then id end) as day4
        , count(distinct case when grass_date = date_add(sign_up_date, interval +5 day) then id end) as day5
        , count(distinct case when grass_date = date_add(sign_up_date, interval +6 day) then id end) as day6
        , count(distinct case when grass_date = date_add(sign_up_date, interval +7 day) then id end) as day7
        , count(distinct case when grass_date = date_add(sign_up_date, interval +8 day) then id end) as day8
        , count(distinct case when grass_date = date_add(sign_up_date, interval +9 day) then id end) as day9
        , count(distinct case when grass_date = date_add(sign_up_date, interval +10 day) then id end) as day10
        , count(distinct case when grass_date = date_add(sign_up_date, interval +11 day) then id end) as day11
        , count(distinct case when grass_date = date_add(sign_up_date, interval +12 day) then id end) as day12
        , count(distinct case when grass_date = date_add(sign_up_date, interval +13 day) then id end) as day13

        , count(distinct case when grass_date between date_add(sign_up_date, interval +1 day) and date_add(sign_up_date, interval +6 day) then id end) as w0
        , count(distinct case when grass_date between date_add(sign_up_date, interval +7 day) and date_add(sign_up_date, interval +13 day) then id end) as w1
        , count(distinct case when grass_date between date_add(sign_up_date, interval +14 day) and date_add(sign_up_date, interval +20 day) then id end) as w2
        , count(distinct case when grass_date between date_add(sign_up_date, interval +21 day) and date_add(sign_up_date, interval +27 day) then id end) as w3
        , count(distinct case when grass_date > date_add(sign_up_date, interval +27 day) then id end) as w4_
from register_table a 
left join tracking_table b on id = user_id 
where true 
  and user_id is not null -- filter users that returned to home screen
  and sign_up_date >= date'2022-08-01'
group by 1,2
order by 2
