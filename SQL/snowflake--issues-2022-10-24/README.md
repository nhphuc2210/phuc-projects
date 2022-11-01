```sql
create or replace TABLE PHUC_DB.PHUC_SCHEMA.test_import (
Column1 varchar,
Column2 varchar,
Column3 varchar,
Column4 varchar,
Column5 varchar,
Column6 varchar,
Column7 varchar,
Column8 varchar,
Column9 varchar,
Column10 varchar,
Column11 varchar,
Column12 varchar,
Column13 varchar,
Column14 varchar,
Column15 varchar,
Column16 varchar,
Column17 varchar,
Column18 varchar,
Column19 varchar,
Column20 varchar,
Column21 varchar,
Column22 varchar,
Column23 varchar,
Column24 varchar,
Column25 varchar,
Column26 varchar,
Column27 varchar,
Column28 varchar,
Column29 varchar
);

select * from PHUC_SCHEMA.test_import

create or replace storage integration phuc_s3
  type = external_stage
  storage_provider = 'S3'
  enabled = true
  storage_aws_role_arn = 'arn:aws:iam::227052876777:role/phuc-snowflake'
  storage_allowed_locations = ('s3://phuc-s3/')
;

DESC INTEGRATION phuc_s3;


CREATE or replace STAGE PHUC_SCHEMA.my_stage 
URL = 's3://phuc-s3/' 
storage_integration = phuc_s3
;

list @PHUC_SCHEMA.my_stage;

create or replace file format CSV_FF
  type = 'CSV'
  field_delimiter = '\t'
  field_optionally_enclosed_by='"'
  ERROR_ON_COLUMN_COUNT_MISMATCH=FALSE
  ;


copy into phuc_db.phuc_schema.test_import
from @PHUC_SCHEMA.my_stage
file_format = CSV_FF
ON_ERROR = SKIP_FILE 
force=True
;


select count(*)
from phuc_db.phuc_schema.test_import



delete from phuc_db.phuc_schema.test_import

drop table phuc_schema.target_table

select * from table(validate(phuc_db.phuc_schema.test_import, job_id=>'01a7d5df-3200-9324-0001-ff9a00034106'));


SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY
order by last_load_time desc 



```



