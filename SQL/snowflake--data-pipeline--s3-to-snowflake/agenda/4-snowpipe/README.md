
# **Configuring Amazon SNS to Automate Snowpipe Using SQS Notifications**


This section describes how to trigger Snowpipe data loads automatically using Amazon SQS (Simple Queue Service)notifications for an S3 bucket

The following diagram shows the process flow for Snowpipe auto-ingest with Amazon SNS:

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\snowflake-4.jpg)

1. Data files are loaded in a stage.

2. An S3 event notification published by SNS informs Snowpipe via an SQS queue that files are ready to load. Snowpipe copies the files into a queue.

3. A Snowflake-provided virtual warehouse loads data from the queued files into the target table based on parameters defined in the specified pipe.


#

<br />

## **Step 1: Create a Stage (If Needed)**

```sql
use schema PHUCDB.PHUC_S;

create stage mystage
  url = 's3://phuc-nguyen/fbcpas_adoption.csv'
  storage_integration = phuc_s3;
```
<br />

## **Step 2: Create a Pipe with Auto-Ingest Enabled**

Create a pipe using the CREATE PIPE command. The pipe defines the COPY INTO <table> statement used by Snowpipe to load data from the ingestion queue into the target table.

Must to create table before ingestion



Copy into created table

```sql

use role accountadmin;
use database phuc_db;
use schema phuc_schema;
use warehouse phuc_wh;


create or replace storage integration phuc_s3
  type = external_stage
  storage_provider = 'S3'
  enabled = true
  storage_aws_role_arn = 'arn:aws:iam::227052876777:role/phuc-snowflake'
  storage_allowed_locations = ('s3://phuc-nguyen/')
//  storage_blocked_locations = ('s3://mybucket1/mypath1/sensitivedata/', 's3://mybucket2/mypath2/sensitivedata/')
;


DESC INTEGRATION phuc_s3;

use schema phuc_db.phuc_schema;

create or replace stage mystage
  url = 's3://phuc-nguyen/adoption/'
  storage_integration = phuc_s3;

list @mystage;

show stages;

create or replace table phuc_db.phuc_schema.mytable (shop_id varchar, grass_date varchar, segment varchar);

select * from phuc_db.phuc_schema.mytable;

DELETE FROM phuc_db.phuc_schema.mytable;

create or replace pipe phuc_db.phuc_schema.mypipe auto_ingest=true as
  
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

SELECT * FROM phuc_db.phuc_schema.mytable;

show pipes;

desc pipe mypipe;

select SYSTEM$PIPE_STATUS('mypipe');

           
select *
from table(information_schema.copy_history(table_name=>'mytable', start_time=> dateadd(hours, -1, current_timestamp())));

alter pipe mypipe refresh;

```

