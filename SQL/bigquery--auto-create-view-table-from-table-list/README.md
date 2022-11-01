
# **Auto Create View Table from Table List**

<br />


### **Job Descriptions:**

    To be copied to a new dataset (dataset name to be given as a parameter), by selecting the tables and filtering the values by the organisation and workspace all the table names remain the same

    - The new dataset should be created by the script.
    - Actually you dont need to even take the dataset name as parameter: you construct it like this: newDataSetName='gds_' + organisationName + workspaceName and basically organisationName + workspaceName are the parameters to the script


## **CLIENT'S FEEDBACK**
> thank you this was great!


## **SOLUTIONS**
<br />

```sql
DECLARE table_name STRING;
DECLARE target_table STRING;
DECLARE new_table STRING;
DECLARE from_table STRING;
DECLARE dataset_name STRING;
DECLARE organisationName STRING;
DECLARE workspaceName STRING;


-- ============= INPUT PARAMETERS ================
SET organisationName = 'orijin';              
SET workspaceName = 'orijin_basic_cacao';     
-- ===============================================

-- SET SCHEMA (DATASET)
SET dataset_name = CONCAT('gds_',organisationName,'_',workspaceName);

-- DELETE OLD LOGIC
DROP SCHEMA IF EXISTS dataset_name CASCADE;

-- CREATE DATASET
EXECUTE IMMEDIATE CONCAT('CREATE SCHEMA IF NOT EXISTS ', dataset_name);

-- GET LIST OF TABLES
CREATE TEMP TABLE tableNames as select table_id from gds.__TABLES__ where table_id not in ('activitycompletions');

-- CREATE SUBTABLES
WHILE (select count(*) from tableNames) >= 1 DO
  SET table_name = (select table_id from tableNames LIMIT 1);
  
  -- build dataset + table name
  SET target_table = CONCAT('gds.' , table_name);
  SET new_table = CONCAT(dataset_name,'.', table_name);
        <EXECUTE TASKS>
  DELETE FROM tableNames where table_id = table_name;
END WHILE;
```

