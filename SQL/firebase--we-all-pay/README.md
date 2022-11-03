
# **We All Pay**

**SQL - BigQuery - Current Project**

So here's the questions I have and their context of what I'd like to have answered:

1. I see a small amount of users being retained and, I want to know what first time users do when they click through the app. So, I'd like to know a ViewController list in order of showing per first time user. That way, I know where to make changes.

* I want to know what first time users do when they click through the app.
* ???? I'd like to know a ViewController list in order of showing per first time user.

2. I'm collecting the event name as to figure out the reason as to why people are using the app. That data is logged like this. This way I can improve App Store texts. I'd like to have this data per language and country setting of the device. So, I can filter on that.

grass_date | event_name | user_id | language | 

3. I'd like have a list of the descriptions that are filled in with the payments as well. Those are collected in about the same. I'd like those per user and per time created.

created_time | user_id | discriptions

4. I'd like to know what intervals are for returning user. I understand that some people use the app once or even twice per year. So the retain graph of the firebase analytics dashboard isn't suiting the needs for this app.

Bigquery : https://console.cloud.google.com/bigquery?authuser=1&project=danh-298607&ws=!1m14!1m4!1m3!1sdanh-298607!2sbquxjob_36335bc4_18428e56d03!3sus-central1!1m4!4m3!1sdanh-298607!2sanalytics_151388888!3sevents_20221029!1m3!3m2!1sdanh-298607!2sanalytics_151388888

Data Studio :  https://datastudio.google.com/u/1/reporting/7d99ea4d-6d91-4afd-a06c-b9c04bb072ea/page/OiX5C/edit


<br />

<br />

```sql
select
PARSE_DATE('%Y%m%d', event_date) as grass_date
, TIMESTAMP_SECONDS(CAST(CAST(event_timestamp as INT64)/1000000 as INT64)) 
, *
from `we-all-pay.analytics_151388888.events_20221030`
where lower(geo.country) = 'vietnam'
  and user_pseudo_id = 'D26BC3041B2C4CE5A3EDD2A8CCD34DDF'
  
```
