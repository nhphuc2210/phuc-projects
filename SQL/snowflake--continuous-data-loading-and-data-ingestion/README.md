
# **Continuous Data Loading & Data Ingestion in Snowflake**

## **Agenda**

<br />

1. Quick Overview of Continuous Data Ingestion
2. SnowPipe Object
3. Trigger Notification
4. SnowPipe Copy History
5. SnowPipe Cost
6. Pausing SnowPipe


<br />

### **1. Quick Overview Of Continuous Data Ingestion** 
1. Stage gets a file
2. AWS SNS Triggers Notification
3. Snowflake queue the msg
4. Pipe consumes the msm & execute copy

*So here, everthing happens within the snowflake scope and we dont need to have any dependency from outside or any cloud provider.*

<br />

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/snowflake--continuous-data-loading-and-data-ingestion/.data/c10-1.png)

### **2. SnowPipe Object**

<br />

> **Set the context**
```sql
//===========================
// set the context
//===========================
use role accountadmin;
use database phuc_db;
use schema phuc_schema;
use warehouse phuc_wh;

alter session set query_tag = 'continuous-data-loading-practice'
```

<br />

> Step 1

> Create our table called ingest_from_s3 before we apply auto ingest

```sql
//======================================================
// Create our table called ingest_from_s3 before we apply auto ingest
//======================================================

CREATE OR REPLACE TABLE PHUC_DB.PHUC_SCHEMA.ingest_from_s3 
("shop_id" VARCHAR,"user_name" VARCHAR,"principal" VARCHAR,"main_cat" VARCHAR,"group_cat" VARCHAR,"is_official_shop" VARCHAR,"is_cb_shop" VARCHAR,"segment" VARCHAR,"grass_month" VARCHAR,"grass_date" VARCHAR,"gas_spending" VARCHAR,"gas_gmv_usd" VARCHAR,"cpas_spending" VARCHAR,"cpas_gmv_usd" VARCHAR,"cpas_outbound_click" VARCHAR,"cpas_impression" VARCHAR,"cpas_orders" VARCHAR,"cpas_click" VARCHAR,"other_investment__trafficvalue" VARCHAR,"shop_platform_gmv" VARCHAR,"shop_platform_orders" VARCHAR,"max_grass_date" VARCHAR);
```

<br />

```sql
//==================================================================================
// Let check the record, it returns 0 rows
//==================================================================================

select * 
from PHUC_DB.PHUC_SCHEMA.ingest_from_s3
```

<br />

```sql
//==================================================================================
// Create CSV format and show the configure. 
// Let modify if it has any issues when we ingest
//==================================================================================

CREATE OR REPLACE FILE FORMAT CSV_FF 
TYPE = CSV
SKIP_HEADER=1
field_optionally_enclosed_by='"'
error_on_column_count_mismatch=false;
SHOW FILE FORMATS;
```

<br />

```sql
//==================================================================================
// Create new stage and show info
//==================================================================================

CREATE OR REPLACE STAGE PHUC_DB.PHUC_SCHEMA.GZ_FROM_S3
URL = 's3://phuc-nguyen/seller-info2/' 
CREDENTIALS = (AWS_KEY_ID = 'AKIATJXLH6PUSA5DP2SP' AWS_SECRET_KEY = '7zjmjHERdVb8Qp56/05FEyF+40IlIvpxoz+0m5po')
FILE_FORMAT = CSV_FF
;
show stages like 'GZ_FROM_S3';
```

<br />

```sql
//==================================================================================
// Show all file from stage
//==================================================================================

list @GZ_FROM_S3;
```

<br />

```sql
//==================================================================================
// Extract row numer from stage folder
//==================================================================================

select count(*)
from @PHUC_DB.PHUC_SCHEMA.GZ_FROM_S3;
```

<br />

```sql
//==================================================================================
// Create PIPE to save copy history
//==================================================================================

create or replace pipe phuc_db.phuc_schema.PIPE_GZ_S3 auto_ingest=false as
copy into phuc_db.phuc_schema.ingest_from_s3
from @phuc_db.phuc_schema.GZ_FROM_S3
file_format = CSV_FF
;
show pipes;
desc pipe PIPE_GZ_S3;
```

<br />

### **3. Trigger Notification**

```sql
//==================================================================================
// resume the pipe to activate pipe
//==================================================================================

alter pipe phuc_db.phuc_schema.PIPE_GZ_S3 refresh;
```

<br />

```sql
//==================================================================================
// To monitor the pipe using systen function called PIPE_STATUS
//==================================================================================

use database phuc_db;
use schema phuc_schema;
select SYSTEM$PIPE_STATUS('PIPE_GZ_S3');

// OR

select * from table(validate_pipe_load(
  pipe_name=> 'PIPE_GZ_S3',
  start_time=> dateadd(hour,-1,current_timestamp())));
```

<br />

```sql
//==================================================================================
// Check table size
//==================================================================================

select count(*) 
from phuc_db.phuc_schema.ingest_from_s3;
```

<br />

### **4. SnowPipe Copy History**


```sql
//==================================================================================
// Check Hitory Ingestion. Data will returns after 2-3 hours when we ingest
// To understand what happened and you can see the the data loading through the pipe statement
// This table captures all the detail about your data loading through the pipe object
// It says that how many that records have been successfully uploaded and how many records have been failed for different reason.
//==================================================================================

SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY A
WHERE TRUE 
    AND pipe_name = 'PIPE_GZ_S3'
    AND A.LAST_LOAD_TIME = (SELECT MAX(B.LAST_LOAD_TIME) FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY B WHERE A.pipe_name = B.pipe_name and a.file_name = b.file_name)
```
<br />

```sql
//==================================================================================
// Compare data loaded and data from stage file
//==================================================================================

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
```
<br />

Note: Data from COPY_HISTORY will be fetched after 2-3 hours

<br />

### **5. SnowPipe Cost**

```sql
//==================================================================================
// LOAD HISTORY
// LOAD HISTORY is another table through which you can also understand the load history.
// It does not show anything related to the pipe and it shows in genaral about all the loading status.
// ==================================================================================

SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY;
```
<br />


```sql
//==================================================================================
// IMPORTANT THINGS
// Metering History talks about all the compute services used to load the data it gives you the credit used by the different compute services. 
// You can see the number of your pipe created and you can see how much credit has been used and how much data has been loaded and how many file has been loaded.
// You also build the report related your snowflake account.
//==================================================================================

SELECT * 
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY;
```
<br />

### **5. Pausing SnowPipe**

What happens if we alter and pause the pipe.

```sql
//==================================================================================
// What happens if we alter and pause the pipe.
//==================================================================================

alter pipe PIPE_GZ_S3 set pipe_execution_paused = true;
```

```sql
//==================================================================================
// Check pipe status
//==================================================================================

select SYSTEM$PIPE_STATUS('PIPE_GZ_S3')
```


```sql
//==================================================================================
// To resume it
//==================================================================================

alter pipe PIPE_GZ_S3 refresh;
```

One important things to notice here, the pipe does not guarantee in which order the files would be loaded.
