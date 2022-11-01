
# **S3 TO SNOWFLAKE**

## **Agenda**

<br />

**1. Manual Ingestion**

<br />

    
```sql


create or replace table phuc_db.phuc_schema.mytable (shop_id varchar, grass_date varchar, segment varchar);

select * from phuc_db.phuc_schema.mytable;


CREATE STAGE "PHUC_DB"."PHUC_SCHEMA".manual_stage 
URL = 's3://phuc-nguyen/adoption/' 
CREDENTIALS = (AWS_KEY_ID = 'AKIATJXLH6PUSWXQRWMI' AWS_SECRET_KEY = '****************************************');





copy into phuc_db.phuc_schema.mytable
from (
      SELECT $1, $2, $3
//          REPLACE($1, '"', '') 
//      , REPLACE(regexp_replace($2,'^\'|\'$'), '"','') 
//      , REPLACE(regexp_replace($3,'^\'|\'$'), '"','')
      FROM @phuc_db.phuc_schema.mystage
//        WHERE $1 IS NOT NULL
     )
file_format = (type='CSV' SKIP_HEADER=1 field_optionally_enclosed_by='"')
force=True
;


select * from phuc_db.phuc_schema.mytable;

```

**2. Automatic Ingestion**

<br />

* Step 1: Configuring Secure Access to Cloud Storage <https://github.com/nhphuc2210/previous-similar-projects/tree/main/data-pipeline--s3-to-snowflake/agenda/1-secure-access-to-s3>


* Step 2: Create the IAM Role in AWS <https://github.com/nhphuc2210/previous-similar-projects/tree/main/data-pipeline--s3-to-snowflake/agenda/2-create-role>

* Step 3: Create a Cloud Storage Integration in Snowflake <https://github.com/nhphuc2210/previous-similar-projects/tree/main/data-pipeline--s3-to-snowflake/agenda/3-create-cloud-storage-intergration-in-snowflake>

* Step 4: Configuring Amazon SNS to Automate Snowpipe Using SQS Notifications <https://github.com/nhphuc2210/previous-similar-projects/tree/main/data-pipeline--s3-to-snowflake/agenda/4-snowpipe>
    

