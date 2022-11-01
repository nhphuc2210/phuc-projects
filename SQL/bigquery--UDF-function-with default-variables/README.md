
# **Write BigQuery UDF**

## **JOB REQUIREMENTS**
<br />


### **Job Descriptions:**

1. Declare variables do not work in Functions (while they work in procedures). So my question is how to assign values to variables in UDF

2. How to run SQL & assign value to a variable in UDF. In my case I want to fetch column encryptedKeyset from external_table_for_decrypted_keys & assign it to FIRST_LEVEL_KEYSET in declare section.

3. So ultimately I want to do is Select descrypt_table_1(column_name ),column2,column3,column4 from table1


Original Script

```sql
CREATE OR REPLACE FUNCTION my_proj.my_dataset.udf_decrypt_column(table_name string, column_name string)
BEGIN
DECLARE KMS_RESOURCE_NAME STRING;
DECLARE FIRST_LEVEL_KEYSET STRING;
SET KMS_RESOURCE_NAME= "gcp-kms://projects/dev/locations/us/keyRings/dev/cryptoKeys/dev-kek";
SET FIRST_LEVEL_KEYSET = (select encryptedKeyset from my_project.my_dataset.external_table_for_decrypted_keys);
SELECT
    AEAD.DECRYPT_STRING( KEYS.KEYSET_CHAIN( KMS_RESOURCE_NAME, from_base64(FIRST_LEVEL_KEYSET))
                        , from_base64(column_name)
                        , "" ) as decrypted_ID
FROM table_name.column_name

```


# **Solutions**

```sql


CREATE OR REPLACE FUNCTION my_schema.DECRYPT_STRING(cell_value string)
RETURNS STRING AS (
  concat("Called DECRYPT_STRING for columns ", cell_value)
);



CREATE OR REPLACE FUNCTION my_schema.udf_decrypt_column(cell_value string)
RETURNS STRING
AS ((
      with variable_KMS_RESOURCE_NAME as (
            SELECT "gcp-kms://projects/dev/locations/us/keyRings/dev/cryptoKeys/dev-kek" as KMS_RESOURCE_NAME
      )

      , variable_FIRST_LEVEL_KEYSET as (
            -- select encryptedKeyset from my_project.my_dataset.external_table_for_decrypted_keys
            select string_field_0 as encryptedKeyset from my_schema.external_table__date_table order by 1 limit 1
      )

      -- SELECT AEAD.DECRYPT_STRING( KEYS.KEYSET_CHAIN( KMS_RESOURCE_NAME, from_base64(FIRST_LEVEL_KEYSET))
      --                             , from_base64(column_name)
      --                           , "" ) as decrypted_ID

      select my_schema.DECRYPT_STRING(cell_value)
      -- select *
      from variable_KMS_RESOURCE_NAME, variable_FIRST_LEVEL_KEYSET
));


select *
from my_schema.date_table;

select my_schema.udf_decrypt_column(cell_value)
from my_schema.date_table;


```