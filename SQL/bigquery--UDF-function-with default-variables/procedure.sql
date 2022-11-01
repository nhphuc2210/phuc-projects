DECLARE KMS_RESOURCE_NAME STRING;
DECLARE FIRST_LEVEL_KEYSET BYTES;



SET KMS_RESOURCE_NAME= "my_key";
-- SET FIRST_LEVEL_KEYSET = from_base64("Cmy_bytes");
SET FIRST_LEVEL_KEYSET = (SELECT mybytes FROM external_table);



select
AEAD.DECRYPT_STRING(
KEYS.KEYSET_CHAIN(KMS_RESOURCE_NAME, FIRST_LEVEL_KEYSET),
from_base64(ID),
"") as decrypted_ID
FROM my_table

