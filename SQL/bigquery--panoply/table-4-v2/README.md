
# **BIGQUERY - ACTIVITIES TRACKING**

## **JOB REQUIREMENTS**
<br />

##### **Here is challenge:** `<link>` : ***<https://www.awesomescreenshot.com/video/11584656?key=d50d4159536f9e69406241ab9e0b09b0>***
<br />


##### **Here is the google sheet I was referencing:** `<link>` : ***<https://docs.google.com/spreadsheets/d/1rJoFb_OYct0LoZpN-pLvUuZDZFnoP6mBJEGJ5FhTEmQ/edit#gid=0>***

<br />

**Here is your script**

<br />

```sql

with 
get_user_device as (
  with raw as (-- replace null data
  select id
  , coalesce(signup_os, 'Unknown') as signup_os
  -- from panoply.postgres_core_user__2
  from panoply.postgres_core_user
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
select 
      date(created_at) as grass_date
      , created_at 
      , user_id
      , app_screen
      , action
      , case 
              when app_screen = 'challenges_screen_details' and action = 'view' then 'A'
              when app_screen = 'challenges_screen_session' and action = 'view' then 'B'
              when app_screen = 'home_screen' and action = 'view' then 'C'
              when app_screen = 'search_screen' and action = 'searched' then 'D'
              when app_screen = 'search_screen' and action = 'view' then 'E'
              when app_screen = 'search_screen' and action = 'tap_search_result' then 'F'
              when app_screen = 'series_screen' and action = 'view' then 'G'
              when app_screen = 'session_screen' and action = 'view' then 'H'
              when app_screen = 'session_screen_short' and action = 'view' then 'I'
            else 'Others' end as letter_code

from `panoply.postgres_tracking_eventtrackingmodel`
where true 
  and user_id is not null  
)

, get_more_session as (
select 
    date(m.created_at) as grass_date,
    m.created_at,
    m.session_id,
    m.status_max,
    m.user_id,
    t.series_type,
    concat(m.created_at, m.session_id, m.status_max, m.user_id, t.series_type) as key_session

from `panoply.postgres_tracking_playerstatusmodel` m
LEFT JOIN `panoply.postgres_series_sessionmodels` s ON m.session_id = s.id 
-- LEFT JOIN (select string_field_0 as series_key, string_field_1 as series_type from `panoply.postgres_series_seriesmodels`) t 
LEFT JOIN `panoply.postgres_series_seriesmodels` t 
  ON t.series_key = substr(s.session_key, 1, length(s.session_key) -2)
)

, fmcdevice as (
  select active as is_active, date_created, user_id
        , RANK() OVER ( PARTITION BY user_id ORDER BY date_created desc) AS is_lastest
  from panoply.postgres_fcm_django_fcmdevice
)

, therapyreminders as (
  select is_active, created_at, user_id, day_of_the_week
        , RANK() OVER ( PARTITION BY user_id ORDER BY created_at desc) AS is_lastest
  from panoply.postgres_reminders_therapyreminders
)

select   
         week_start
        , sign_up_date
        , FORMAT_DATE("%m", sign_up_date) as sign_up_month
        , gender
        , age
        , signup_os

        , count(distinct id) as total
        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'C' then id end) as view_home_screen

        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'G' then id end) as view_standard_series
        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'H' then id end) as view_standard_session
        , count(distinct case when a.sign_up_date = c.grass_date and status_max in ('completed_session','continue_playing_session') and series_type = 'Standard' then id end) as play_standard_session
        , count(distinct case when status_max in ('completed_session') and series_type = 'Standard' then id end) as finish_standard_session

        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'A' then id end) as view_challenge_series
        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'B' then id end) as view_challenge_session
        , count(distinct case when a.sign_up_date = c.grass_date and status_max in ('completed_session','continue_playing_session') and series_type = 'Challenge' then id end) as play_challenge_session
        , count(distinct case when a.sign_up_date = c.grass_date and status_max in ('completed_session') and series_type = 'Challenge' then id end) as finish_challenge_session

        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'I' then id end) as view_short_session
        , count(distinct case when a.sign_up_date = c.grass_date and status_max in ('completed_session','continue_playing_session') and series_type = 'Short' then id end) as play_short_session
        , count(distinct case when a.sign_up_date = c.grass_date and status_max in ('completed_session') and series_type = 'Short' then id end) as finish_short_session

        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'D' then id end) as search_screen_searched
        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'E' then id end) as search_screen_view
        , count(distinct case when a.sign_up_date = b.grass_date and letter_code = 'F' then id end) as search_screen_tap_search_result

        , count(distinct case when a.sign_up_date = b.grass_date and ((letter_code = 'G') or (letter_code = 'A') or (letter_code = 'I')) then id end) view_any_series
        , count(distinct case when a.sign_up_date = b.grass_date and ((letter_code = 'H') or (letter_code = 'B') or (letter_code = 'I')) then id end) view_any_session

        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and (status_max in ('completed_session','continue_playing_session') 
                                      and series_type in ('Standard','Challenge','Short')) 
                                    then id end) as play_any_session

        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and (status_max in ('completed_session') 
                                      and series_type in ('Standard','Challenge','Short')) 
                                    then id end) as finish_any_session

-- ====================== NEW 2022-10-07
-- ====================== count distinct users

-- ====================== any sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                    then id end) as users_starting_session_day_0

        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and status_max in ('completed_session') 
                                    then id end) as users_finishing_session_day_0

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                    then id end) as users_starting_session_first_7_days

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                    then id end) as users_finishing_session_first_7_days

-- ====================== standard sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Standard' 
                                    then id end) as users_starting_session_day_0_standard

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Standard' 
                                    then id end) as users_finishing_session_day_0_standard

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Standard' 
                                    then id end) as users_starting_session_first_7_days_standard

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Standard' 
                                    then id end) as users_finishing_session_first_7_days_standard

-- ====================== challenge sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Challenge' 
                                    then id end) as users_starting_session_day_0_challenge

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Challenge' 
                                    then id end) as users_finishing_session_day_0_challenge

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Challenge' 
                                    then id end) as users_starting_session_first_7_days_challenge

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Challenge' 
                                    then id end) as users_finishing_session_first_7_days_challenge

-- ====================== short sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Short' 
                                    then id end) as users_starting_session_day_0_short

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Short' 
                                    then id end) as users_finishing_session_day_0_short

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Short' 
                                    then id end) as users_starting_session_first_7_days_short

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Short' 
                                    then id end) as users_finishing_session_first_7_days_short


-- ====================== count distinct sessions

-- ====================== any sessions
-- ====================== any sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                    then key_session end) as number_sessions_started_day_0

        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and status_max in ('completed_session') 
                                    then key_session end) as number_sessions_finished_day_0

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                    then key_session end) as number_sessions_started_first_7_days

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                    then key_session end) as number_sessions_finished_first_7_days

-- ====================== standard sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Standard' 
                                    then key_session end) as number_sessions_started_day_0_standard

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Standard' 
                                    then key_session end) as number_sessions_finished_day_0_standard

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Standard' 
                                    then key_session end) as number_sessions_started_first_7_days_standard

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Standard' 
                                    then key_session end) as number_sessions_finished_first_7_days_standard

-- ====================== challenge sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Challenge' 
                                    then key_session end) as number_sessions_started_day_0_challenge

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Challenge' 
                                    then key_session end) as number_sessions_finished_day_0_challenge

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Challenge' 
                                    then key_session end) as number_sessions_started_first_7_days_challenge

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Challenge' 
                                    then key_session end) as number_sessions_finished_first_7_days_challenge

-- ====================== short sessions
        , count(distinct case when a.sign_up_date = c.grass_date 
                                      and series_type = 'Short' 
                                    then key_session end) as number_sessions_started_day_0_short

        , count(distinct case when a.sign_up_date = c.grass_date
                                      and status_max in ('completed_session') 
                                      and series_type = 'Short' 
                                    then key_session end) as number_sessions_finished_day_0_short

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and series_type = 'Short' 
                                    then key_session end) as number_sessions_started_first_7_days_short

        , count(distinct case when c.grass_date between a.sign_up_date and date_add(a.sign_up_date , interval +6 day)
                                      and status_max in ('completed_session') 
                                      and series_type = 'Short' 
                                    then key_session end) as number_sessions_finished_first_7_days_short


-- ====================== short sessions

        , count(distinct d.user_id) as push_active_ever
        , count(distinct e.user_id) as therapy_reminders_active_ever
        , count(distinct case when d.user_id = e.user_id then a.id end) as both_on_ever

        , count(distinct case when d.is_active = true and d.is_lastest = 1 then d.user_id end) as push_active_now
        , count(distinct case when e.is_active = true and e.is_lastest = 1 then e.user_id end) as therapy_reminders_active_now
        , count(distinct case when d.user_id = e.user_id and e.is_active = true and d.is_active = true and d.is_lastest = 1 and e.is_lastest = 1 then a.id end) as both_on_now

from register_table a 
left join tracking_table b on id = b.user_id --and a.sign_up_date = b.grass_date -- GET letter_code // get view session
left join get_more_session c on a.id = c.user_id --and a.sign_up_date = c.grass_date -- GET status_max, series_type // get play session
left join fmcdevice d on a.id = d.user_id
left join therapyreminders e on a.id = e.user_id

where true 
  and sign_up_date = date'2022-09-20'
group by 1,2,3,4,5,6
order by 2

```
