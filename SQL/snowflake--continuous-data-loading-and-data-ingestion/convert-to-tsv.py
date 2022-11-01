
import pandas as pd 


df = pd.read_csv(r'sql-snowflake--continuous-data-loading-and-data-ingestion\2022010100_data_102_4_0.csv',header=None)

df.to_csv(r'sql-snowflake--continuous-data-loading-and-data-ingestion\my_tsv_file.tsv.gz', sep="\t", index=False, compression='gzip',header=False)

