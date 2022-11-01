
# **Download Snowflake > 100MB to local WINDOWS**

<br />

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/snowflake--download-more-than-100-mb/.data/stage_file.png)



## **Pre-requisite**
<br />

> 1. Install Snowflake CLI to run SnowSQL commands.
> 2. Extract data needed to stage files

```sql 
CREATE OR REPLACE STAGE PHUCDB.PHUC_S.my_temp_stage;

COPY INTO @my_temp_staged
FROM (
-- INPUT YOUR QUERY RESULT IN HERE

    select hashed_email, date, domain
    from database.schema.table_name
    where true
        and hashed_email is not null
        and date between date'2022-08-01' and current_date
        and regexp_like( lower(domain) , 'domainA|domainB')


)
FILE_FORMAT = (
TYPE='CSV'
COMPRESSION=GZIP
FIELD_DELIMITER=','
ESCAPE=NONE
ESCAPE_UNENCLOSED_FIELD=NONE
date_format='AUTO'
time_format='AUTO'
timestamp_format='AUTO'
binary_format='UTF-8'
field_optionally_enclosed_by='"'
null_if=''
EMPTY_FIELD_AS_NULL = FALSE
)
overwrite=TRUE
single=FALSE
max_file_size=5368709120
header=TRUE;



ls @my_temp_stage;

```

<br />

<br />

## **Download**
<br />

**Step 1: Connect to Snowflake database and schema**

```
snowsql -a host -u username
```
**Step 2: Input password**

**Step 3: Select DataBase, Schema, Warehouse**

```
use database aaa
```

**Step 4: Download**

```
GET @my_temp_stage file://C:\Users\Administrator\Downloads\
```





