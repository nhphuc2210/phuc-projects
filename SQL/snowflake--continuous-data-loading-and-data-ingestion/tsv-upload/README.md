
## **File tsv in s3 folder**
 
![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/sql-snowflake--continuous-data-loading-and-data-ingestion/tsv-upload/1-tsv-file.jpg)


## **Script for file format TSV**

```sql
CREATE OR REPLACE FILE FORMAT TSV_FF 
TYPE = CSV
SKIP_HEADER=0
FIELD_DELIMITER='\t'
field_optionally_enclosed_by='"'
error_on_column_count_mismatch=false;
SHOW FILE FORMATS;
```

## **Loaded successfully**

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/sql-snowflake--continuous-data-loading-and-data-ingestion/tsv-upload/2-copied-successfully.jpg)
