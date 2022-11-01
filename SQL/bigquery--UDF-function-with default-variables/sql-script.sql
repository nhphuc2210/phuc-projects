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
