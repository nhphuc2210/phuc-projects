
```sql

CREATE OR REPLACE TABLE PHUC_DB.PHUC_SCHEMA.ingest_from_s3 ("shop_id" VARCHAR,"user_name" VARCHAR,"principal" VARCHAR,"main_cat" VARCHAR,"group_cat" VARCHAR,"is_official_shop" VARCHAR,"is_cb_shop" VARCHAR,"segment" VARCHAR,"grass_month" VARCHAR,"grass_date" VARCHAR,"gas_spending" VARCHAR,"gas_gmv_usd" VARCHAR,"cpas_spending" VARCHAR,"cpas_gmv_usd" VARCHAR,"cpas_outbound_click" VARCHAR,"cpas_impression" VARCHAR,"cpas_orders" VARCHAR,"cpas_click" VARCHAR,"other_investment__trafficvalue" VARCHAR,"shop_platform_gmv" VARCHAR,"shop_platform_orders" VARCHAR,"max_grass_date" VARCHAR);


select * from PHUC_DB.PHUC_SCHEMA.ingest_from_s3


CREATE OR REPLACE FILE FORMAT CSV_FF 
TYPE = CSV
SKIP_HEADER=1
field_optionally_enclosed_by='"'
error_on_column_count_mismatch=false;
SHOW FILE FORMATS;


CREATE OR REPLACE STAGE PHUC_DB.PHUC_SCHEMA.GZ_FROM_S3
URL = 's3://phuc-nguyen/seller-info2/' 
CREDENTIALS = (AWS_KEY_ID = 'AKIATJXLH6PUSA5DP2SP' AWS_SECRET_KEY = '7zjmjHERdVb8Qp56/05FEyF+40IlIvpxoz+0m5po')
FILE_FORMAT = CSV_FF
;



show stages like 'GZ_FROM_S3';

list @GZ_FROM_S3;

select count(*)
from @PHUC_DB.PHUC_SCHEMA.GZ_FROM_S3;


TRUNCATE phuc_db.phuc_schema.GZ_LARGE_TEST

create or replace pipe phuc_db.phuc_schema.PIPE_GZ_S3 auto_ingest=false as
copy into phuc_db.phuc_schema.ingest_from_s3
from @phuc_db.phuc_schema.GZ_FROM_S3
file_format = CSV_FF
;

desc pipe PIPE_GZ_S3;

show pipes like 'PIPE_GZ_S3';

select * from PHUC_DB.PHUC_SCHEMA.ingest_from_s3

alter pipe phuc_db.phuc_schema.PIPE_GZ_S3 refresh;

use database phuc_db;
use schema phuc_schema;
select SYSTEM$PIPE_STATUS('PIPE_GZ_S3');

select * from table(validate_pipe_load(
  pipe_name=> 'PIPE_GZ_S3',
  start_time=> dateadd(hour,-1,current_timestamp())));
           
select count(*) from phuc_db.phuc_schema.ingest_from_s3;

list @GZ_FROM_S3;


with loaded_file_name as (
SELECT FILE_NAME
FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY A
WHERE TRUE 
    AND pipe_name = 'PIPE_GZ_S3'
    AND A.LAST_LOAD_TIME = (SELECT MAX(B.LAST_LOAD_TIME) FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY B WHERE A.pipe_name = B.pipe_name and a.file_name = b.file_name)
    and row_count = row_parsed
)

, stage_file_name as (
select split_part(metadata$filename, '/',2) as file_name
from @GZ_FROM_S3
)

select *
from stage_file_name a 
left join loaded_file_name b on a.file_name = b.file_name
where b.file_name is null

SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY;


SELECT * 
FROM SNOWFLAKE.ACCOUNT_USAGE.STAGES;



SELECT * 
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY;



```