#standardSQL
--interaction table
with table2 as
    (SELECT * EXCEPT (interactions_validity)
     FROM (select p.*
                , q.hybris_id
                , q.model
                , q.market_area
                --************CASE here to filter out invalid interactions for 2022 products i.e interactions logged before official eng start date************************
                , CASE
                      WHEN q.model IN ('S21FE') AND p.ia_date < DATE('2022-01-03') THEN 'invalid'
                      WHEN q.model IN ('S22') AND p.ia_date < DATE('2022-01-26') THEN 'invalid'
                      ELSE 'valid' END AS interactions_validity
           from (select a.*, b.country
                 from (select *
                       from gcdm.interactions_full
                       where ia_type in
                             ('EMAIL_OUTBOUND', 'PUSH_OUTBOUND', 'EMAIL_OPENED', 'PUSH_CLICK', 'PUSH_DELIVERED',
                              'CLICK_THROUGH')
                         --**************************************************************
                         and ia_date between @eng_startdate and @eng_enddate) a
                          inner join gcdm.customers b
                                     on a.gcdm_customer_id = b.id) p
                    inner join
                --MTD campaigns
                    (select distinct hybris_id,
                                     market_area,
                                     case
                                         when model1 in ('A', 'J', 'M') then 'A'
                                         when model1 in ('FLIP3', 'FOLD3') then 'Z3'
                                         when model1 in ('S21', 'S21FE') then 'S21FE'
                                         else model1 end as model
                     from (select hybris_id
                                , model                as model1
                                , market_area
                                --************CASE here to filter out invalid campaigns (run before official eng start) ************************
                                , CASE
                                      WHEN model IN ('S21FE', 'S21') AND date < DATE('2022-01-03') THEN 'invalid'
                                      WHEN model IN ('S22') AND date < DATE('2022-01-26') THEN 'invalid'
                                      ELSE 'valid' END AS cmpg_validity
                           from gcdm.campaigns
                                --**********************************************************************
                           where date between @eng_startdate and @eng_enddate
                             and model is not null
                             and hybris_id is not null)
                     WHERE cmpg_validity IN ('valid')) q
                on p.campaign_id = q.hybris_id
                    and p.country = q.market_area)
     WHERE interactions_validity IN ('valid'))

   , age_exclusion as
    (select *
     from (select distinct id                                             as gcdm_customer_id,
                           country,
                           birth_year,
                           EXTRACT(YEAR from @reg_startdate) - birth_year as age
           from gcdm.customers
           where country in ('TH'))
     where age <= 19
        or birth_year is null
     union all
     select *
     from (select distinct id                                             as gcdm_customer_id,
                           country,
                           birth_year,
                           EXTRACT(YEAR from @reg_startdate) - birth_year as age
           from gcdm.customers
           where country not in ('KH', 'LA', 'MM', 'TW'))
     where age <= 17)

SELECT country
     , model
     , count(distinct gcdm_customer_id)   as tgt_total
     , sum(engaged)                       as eng_total
     , sum(edm_open)                      as edm_open_total
     , sum(edm_click)                     as edm_click_total
     , EXTRACT(MONTH FROM @reg_startdate) AS month
     , SUM(comms_cnt)                     AS num_of_comms
     , EXTRACT(YEAR FROM @reg_startdate)  AS Year
from (
         --people who are targeted
         select a.*, b.engaged, c.edm_click, d.edm_open, e.comms_cnt
         from (select distinct gcdm_customer_id, model, country
               from table2
               where ia_type in ('EMAIL_OUTBOUND', 'PUSH_OUTBOUND', 'PUSH_DELIVERED')
                 and gcdm_customer_id not in
                     (select distinct gcdm_customer_id
                      from age_exclusion)
                 and country not in ('KH', 'LA', 'MM', 'TW')) a
                  --engaged flag
                  left outer join
              (select distinct gcdm_customer_id, model, 1 as engaged
               from table2
               where ia_type in ('EMAIL_OPENED', 'PUSH_CLICK')) b
              on a.gcdm_customer_id = b.gcdm_customer_id
                  and a.model = b.model
                  --email click flag
                  left outer join
              (select distinct gcdm_customer_id, model, 1 as edm_click
               from table2
               where ia_type in ('CLICK_THROUGH')) c
              on a.gcdm_customer_id = c.gcdm_customer_id
                  and a.model = c.model
                  --email opened flag
                  left outer join
              (select distinct gcdm_customer_id, model, 1 as edm_open
               from table2
               where ia_type in ('EMAIL_OPENED')) d
              on a.gcdm_customer_id = d.gcdm_customer_id
                  and a.model = d.model
                  --JOIN for comms count
                  LEFT JOIN
              (select gcdm_customer_id, model, country, count(hybris_id) as comms_cnt
               from table2
               where ia_type in ('EMAIL_OUTBOUND', 'PUSH_OUTBOUND', 'PUSH_DELIVERED')
               GROUP BY gcdm_customer_id, model, country) e
              on a.gcdm_customer_id = e.gcdm_customer_id
                  and a.model = e.model)
WHERE model in ('Z3', 'S22', 'S21FE', 'A', 'TV', 'WM', 'REF')
  AND country not in ('KH', 'LA', 'MM', 'TW')
group by country, model
order by country, model asc