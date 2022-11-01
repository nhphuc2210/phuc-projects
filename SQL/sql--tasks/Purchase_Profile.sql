with prod_hist as
(
  select *, row_number() over (partition by gcdm_customer_id order by act_reg_date desc, model, cat1, cat2, cat3 desc) as prod_num
  from
  (
    select gcdm_customer_id, model, cat1, cat2, cat3, min(reg_date) as act_reg_date 
    from gcdm.products
    where reg_date is not null
    group by gcdm_customer_id, model, cat1, cat2, cat3
  )
),

-- in month total buyers
inmonth_buyers as 
(
	SELECT * EXCEPT(purchase_validity)
	FROM
	(
		select 
			market
			,product_type
			,gcdm_customer_id
			,optin_channel
			,act_reg_date
--************CASE here to filter out invalid purchases for 2022 products i.e products registered before official reg start date************************
			,CASE WHEN product_type IN ('S21FE') AND act_reg_date < DATE('2022-01-11') THEN 'invalid'
			WHEN product_type IN ('S22') AND act_reg_date < DATE('2022-03-04') THEN 'invalid'
			ELSE 'valid' END AS purchase_validity	
		from
		(
			select *, 
			case when cat2= 'Smart Phone' THEN IM_group
			else cat1 end as product_type
			from
			(
				select a.*, b.product_group2 as IM_group,c.country as market,c.optin_channel 
				from
				(
					select * from prod_hist
					-- ***************************************************************
					where act_reg_date between @reg_startdate and @reg_enddate
				)a
				left outer join 
				--A,J,S10 flag
				(
					select 
						cat3
						,case when product_group in ('A','J','M') THEN 'A' 
						when product_group in ('FLIP3','FOLD3') then 'Z3'
						else product_group end as product_group2
					from
					(
						select cat3,product_group2 as product_group 
						from IRIS.cat3_mapping
					)
				)b
				on a.cat3=b.cat3
				inner join 
				gcdm.customers c
				on a.gcdm_customer_id = c.id
			)
		)
		where product_type in ('Z3','A','S22','S21FE','TV','REF','WM')
		and market not in ('KH','LA','MM','TW') 
	)
	WHERE purchase_validity IN ('valid')
),

--interaction table
table1 as
(
	SELECT * EXCEPT(interactions_validity)
	FROM 
	(
		select 
		p.*
		,q.hybris_id
		, q.model
		, q.market_area
	--************CASE here to filter out invalid interactions for 2022 products i.e interactions logged before official eng start date************************
		,CASE WHEN q.model IN ('S21FE') AND p.ia_date < DATE('2022-01-03') THEN 'invalid'
		WHEN q.model IN ('S22') AND p.ia_date < DATE('2022-01-26') THEN 'invalid'
		ELSE 'valid' END AS interactions_validity	
	  from
	  (
		select a.*, b.country
		from
		(
		  select *
		  from gcdm.interactions_full
		  where ia_type in ('EMAIL_OUTBOUND','PUSH_OUTBOUND','EMAIL_OPENED','PUSH_CLICK','PUSH_DELIVERED','CLICK_THROUGH')
		  --**************************************************************
		  and ia_date between @eng_startdate and @eng_enddate
		) a
		inner join gcdm.customers b
		on a.gcdm_customer_id = b.id
	  )p
	  inner join
	  --YTD campaigns
	  (
	  select distinct hybris_id, market_area, 
	  case when model1 in ('A','J','M') then 'A' 
	  when model1 in ('FLIP3', 'FOLD3') then 'Z3' 
	  when model1 in ('S21', 'S21FE') then 'S21FE' else model1 end as model
	  from
		(
		select 
			hybris_id
			, model as model1
			, market_area
--************CASE here to filter out invalid campaigns (run before official eng start) ************************
			,CASE WHEN model IN ('S21FE','S21') AND date < DATE('2022-01-03') THEN 'invalid'
			WHEN model IN ('S22') AND date < DATE('2022-01-26') THEN 'invalid'
			ELSE 'valid' END AS cmpg_validity
		from gcdm.campaigns
		--**********************************************************************
		where date between @eng_startdate and @eng_enddate
		and model is not null 
		and hybris_id is not null
		)
		WHERE cmpg_validity IN ('valid')
	  )q
	  on p.campaign_id = q.hybris_id
	  and p.country = q.market_area
	)
	WHERE interactions_validity IN ('valid')
)

--***********************************
select
    EXTRACT(MONTH FROM @reg_startdate) AS month
    ,market
    ,product_type
    ,count(distinct gcdm_customer_id) as total_byrs
    ,sum(engaged_buyer) as eng_byr
    ,sum(ret_noteng) as not_eng_byr
    ,sum(ret_opt_out) as opt_out_byr
    ,sum(ret_not_targ_cont) as not_targ_cont_byr
    ,sum(ret_not_targ_not_cont) as not_targ_not_cont_byr
    ,sum(acq) as acquisition_byr
    ,EXTRACT(YEAR FROM @reg_startdate) AS year
from
(
  select 
    *,
    case when engaged = 1 then 1 else 0 end as engaged_buyer,
	case when targeted = 1 and engaged is null then 1 else 0 end as ret_noteng,
	case when targeted is null and engaged is null and retention = 1 and optin is null then 1 else 0 end as ret_opt_out,
	case
		when market in ('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is not null and age > 19 then 1
		when market not in('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is not null and age > 17 then 1
		when market in ('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is null then 0 --new
		when market not in ('TH')and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is null then 1 --new
		else 0
	end as ret_not_targ_cont,
	case
		when market in ('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is not null and age <= 19 then 1
		when market not in('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is not null and age <= 17 then 1
		when market in ('TH') and targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is not null and birth_year is null then 1 --new
		when targeted is null and engaged is null and retention = 1 and optin = 1 and sha256_email is null then 1 else 0
	end as ret_not_targ_not_cont,
	case when targeted is null and engaged is null and retention is null then 1 else 0 end as acq
  from
  (
  select k.*
  from
	  (
	  select h.*, i.sha256_email
	  from
	  (
	  select *
	  from 
	  (
		  select gcdm_customer_id, product_type, market, retention, optin, targeted, engaged, birth_year, EXTRACT(YEAR from @reg_startdate) - birth_year as age
		  from
		  (
			select * from
			(
				select a.*,b.retention, c.optin, d.targeted, e.engaged, f.birth_year
				from
				(
					select gcdm_customer_id, product_type, market , count(*)
					from inmonth_buyers
					group by gcdm_customer_id, product_type, market
				) a
				left outer join 
				--retention flag
				(
				  select  gcdm_customer_id, 1 as retention , count(*)
				  from gcdm.products 
				  --*****************************************************************
				  where reg_date < @reg_startdate
				  group by gcdm_customer_id, retention
				)b
				on a.gcdm_customer_id =b.gcdm_customer_id
				-- optin flag
				left outer join
                (
                    select gcdm_customer_id, 1 as optin , count(*)
                    from
                    (
                        select *
                        from
                        (
                            SELECT *,
                            CASE 
                                WHEN reg_month2 = 1 THEN 12
                                ELSE reg_month2 -1
                            END AS reg_month
                            FROM
                            (
                                SELECT *,
                                EXTRACT(month FROM DATE(data_date)) AS month, EXTRACT(month FROM @reg_startdate) AS reg_month2
                                FROM gcdm.opt_status_all
                                WHERE optin_channel IN ('Y')
                                AND DATE(data_date) between DATE_SUB(@reg_startdate, INTERVAL 3 month) AND @reg_enddate
                            )
                        )
                        where month = reg_month
                    )
                    group by gcdm_customer_id, optin
                )c
                on a.gcdm_customer_id = c.gcdm_customer_id
				--targeted flag
				left outer join
				(
				  select gcdm_customer_id, model, 1 as targeted , count(*)
				  from table1
				  where ia_type in ('EMAIL_OUTBOUND','PUSH_OUTBOUND','PUSH_DELIVERED')
				  group by gcdm_customer_id, model, targeted
				) d
				on a.gcdm_customer_id = d.gcdm_customer_id
				and a.product_type = d.model
				--engaged flag (Owned)
				left outer join
				(
				  select gcdm_customer_id,model, 1 as engaged , count(*)
				  from table1
				  where ia_type in ('EMAIL_OPENED','PUSH_CLICK')
				  group by gcdm_customer_id,model, engaged
				) e
				on a.gcdm_customer_id = e.gcdm_customer_id
				and a.product_type=e.model
				left outer join
				(
					select distinct id, birth_year
					from gcdm.customers
				) f
				on a.gcdm_customer_id = f.id 
			)			
		  ) 
		  group by gcdm_customer_id, product_type, market, retention, optin, targeted, engaged, birth_year
	   )
	  )h
	  left join gcdm.hashed_customers i
	  on h.gcdm_customer_id = i.id
	 )k
	
 )
)
group by market, product_type
order by market, product_type