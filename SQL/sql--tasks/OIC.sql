	#StandardSQL
	with age_exclusion as
	(
		select *
		from
		(
			select distinct id as gcdm_customer_id, country, birth_year, EXTRACT(YEAR from @reg_startdate) - birth_year as age
			from gcdm.customers
			where country in ('TH')
		)
		where age <= 19 or birth_year is null
		union all
		select *
		from
		(
			select distinct id as gcdm_customer_id, country, birth_year, EXTRACT(YEAR from @reg_startdate) - birth_year as age
			from gcdm.customers
			where country not in ('KH','LA','MM','TW') 
		)
		where age <= 17
	)
	
	select extract(month from @reg_startdate) as month,
	market, 
	count(distinct id) as total_cust,
	sum(ret_cont_cust) as ret_cont_customer,
	extract(year from @reg_startdate) as year
	from
	(
		select 
		*,
		case
		when market in ('TH') and retention = 1 and sha256_email is not null and optin = 1 and birth_year is not null and age > 19 then 1
		when market not in ('TH') and retention = 1 and sha256_email is not null and optin = 1 and birth_year is not null and age > 17 then 1
		when market not in ('TH') and retention = 1 and optin = 1 and sha256_email is not null and birth_year is null then 1
		else 0
		end as ret_cont_cust
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
						select id, market, retention, optin, birth_year, EXTRACT(YEAR from @reg_startdate) - birth_year as age
						from
						(
							select p.*from
							(
								select a.*,b.retention, c.optin, d.birth_year
								from
								(
									select id, country as market , count(*)
									from gcdm.customers
									where id not in
									(
										select distinct gcdm_customer_id
										from age_exclusion
									)
									group by id, country
								) a
								left outer join 
								--retention flag
								(
									select gcdm_customer_id, retention, count(*)
									from
									(
										select gcdm_customer_id, 1 as retention
										from
										(
											select  gcdm_customer_id, 1 as retention
											from gcdm.products 
											--*****************************************************************
											where reg_date < @reg_startdate
											group by gcdm_customer_id, retention
										)
										union all
										(
											select gcdm_customer_id, 1 as retention
											from gcdm.interactions_full
											where ia_date < @reg_startdate
											and ia_type in ('EMAIL_OUTBOUND', 'PUSH_OUTBOUND','PUSH_DELIVERED')
											group by gcdm_customer_id, retention
										)
									)
									group by gcdm_customer_id, retention
								)b
								on a.id =b.gcdm_customer_id
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
												WHEN reg_month2 = 2 THEN reg_month2 -1
												WHEN reg_month2 = 3 THEN reg_month2 -1
												WHEN reg_month2 = 4 THEN reg_month2 -1
												WHEN reg_month2 = 5 THEN reg_month2 -1
												WHEN reg_month2 = 6 THEN reg_month2 -1
												WHEN reg_month2 = 7 THEN reg_month2 -1
												WHEN reg_month2 = 8 THEN reg_month2 -1
												WHEN reg_month2 = 9 THEN reg_month2 -1
												WHEN reg_month2 = 10 THEN reg_month2 -1
												WHEN reg_month2 = 11 THEN reg_month2 -1
												WHEN reg_month2 = 12 THEN reg_month2 -1
											END AS reg_month
											FROM
											(
												SELECT *,
												EXTRACT(month FROM DATE(data_date)) AS month, EXTRACT(month FROM @reg_startdate) AS reg_month2
												FROM gcdm.opt_status_all
												WHERE optin_channel IN ('Y')
												AND DATE(data_date) between DATE_SUB(@reg_startdate, INTERVAL 11 month) AND @reg_enddate
											)
										)
										where month = reg_month
									)
									group by gcdm_customer_id, optin
								)c
								on a.id = c.gcdm_customer_id
								left outer join
								(
									select distinct id, birth_year
									from gcdm.customers
								)d
								on a.id = d.id
							)p
						) 
					)
				)h
				left join gcdm.hashed_customers i
				on h.id = i.id
			)k
		)
	)
	where market not in ('KH','LA','MM','TW')
	group by market
	order by market