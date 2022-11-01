
# **BIGQUERY - RETENTION REPORT**

## **JOB REQUIREMENTS**
<br />

##### **Here is challenge:** `<link>` : ***<https://www.awesomescreenshot.com/video/11356702?key=9254642cdc78d12c6f07e5138f6a1a6c>***
<br />


##### **Here is the google sheet I was referencing:** `<link>` : ***<https://www.awesomescreenshot.com/video/11356702?key=9254642cdc78d12c6f07e5138f6a1a6c>***

<br />

**Here is your script**

<br />

```sql
with 
get_user_device as (
  with raw as (-- replace null data
  select id
  , coalesce(signup_os, 'Unknown') as signup_os
  from panoply.postgres_core_user__2
  )

  , add_rank as (
    select id, signup_os, RANK() OVER ( PARTITION BY id ORDER BY signup_os ) AS rank
    from raw 
  )

  select id	, signup_os
  from add_rank
  where rank = 1
)

, user_profile as (
  with raw as (-- replace null data
  select user_id
  , coalesce(age, 'Unknown') as age
  , coalesce(gender, 'Unknown') as gender
  , created_at
  from panoply.postgres_onboarding_onboardingusermodels
  )

  , add_rn as (-- add rn
    select user_id, age, gender, RANK() OVER ( PARTITION BY user_id ORDER BY created_at ) AS rn
    from raw 
  )

  select user_id, age, gender
  from add_rn
  where rn = 1
)

, register_table as (
  SELECT
      a.id
    , created_at
    , DATE(created_at) AS sign_up_date
    , date(DATE_TRUNC(created_at, week(MONDAY))) as week_start
    
    , coalesce(signup_os, 'Unknown') signup_os
    , coalesce(age, 'Unknown') age
    , coalesce(gender, 'Unknown') gender

  FROM `panoply.postgres_core_user` a 
  left join get_user_device b on a.id = b.id
  left join user_profile c on a.id = c.user_id 
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
        , FORMAT_DATE("%m", sign_up_date) as month
        , gender
        , age
        , signup_os

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
  and sign_up_date = date'2022-08-01'
group by 1,2,3,4,5,6


```