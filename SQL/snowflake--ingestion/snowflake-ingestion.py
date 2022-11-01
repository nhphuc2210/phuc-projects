#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

sys.path.append("..")
# from common.util.database.snowflake import SnowflakeLoader
# from common.loader.excel_loader.util import source_to_parquet
import argparse
import os
# from common.constant.mode import ETLMode
import logging
# license_hp_service = 'C:/cloud_service'
# sys.path.append(license_hp_service)
# import hoangphuc__function

# # Snowflake
#

# In[2]:


from snowflake import connector
from os import getenv



class SnowflakeLoader:
   def __init__(self, schema, target_table):
       self.schema = schema.upper()
       self.cred = self.get_cred()
       self.cred["schema"] = self.schema
       self.cur = self.connect(self.cred)
       self.target_table = target_table.upper()
       self.target_stg_table = f"{target_table}_STG"

   def get_cred(self):
       return {
           "user": getenv("dwh_username","Natalie" ),
           "password": getenv("dwh_password", "Natalie123"),
           "account": getenv("dwh_account", "zb10016.ap-southeast-1"),
           "role": getenv("dwh_role",'X_BAS_BI_USER'),
           "database": getenv("dwh_database", "DWH"),
       }

   def connect(self, cred):
       self.conn = connector.connect(**cred)
       return self.conn.cursor()

   def get_columns(self, tablename):
       result = self.cur.execute(
           f"""SELECT
       COLUMN_NAME , DATA_TYPE
       FROM INFORMATION_SCHEMA.COLUMNS
       WHERE TABLE_SCHEMA = '{self.schema}'
       AND TABLE_NAME = '{tablename}'"""
       ).fetchall()

       return {x[0]: x[1] for x in result}

   def create_table(self, col_definition, table=None):

       if table is None:
           table = self.target_table

       return self.cur.execute(
           f"CREATE TABLE IF NOT EXISTS {table} ({col_definition});"
       ).fetchone()

   def add_column(self, colname, datatype):
       return self.cur.execute(
           f"ALTER TABLE {self.target_table} ADD {colname} {datatype}"
       ).fetchone()

   def put_file(self, path):
       return self.cur.execute(
           f"put file://{path} @{self.target_stg_table};"
       ).fetchone()

   def create_stg_table(self):
       return self.cur.execute(
           f"CREATE OR REPLACE STAGE {self.target_stg_table} file_format = (type = 'PARQUET');"
       ).fetchone()

   def close(self):
       self.cur.close()
       self.conn.close()

   def drop_table(self, table):
       return self.cur.execute(f"DROP TABLE IF EXISTS {table}").fetchone()

   def table_def_update(self):
       target_cols = self.get_columns(self.schema, self.target_table)
       stg_cols = self.get_columns(self.schema, self.target_stg_table)

       new_cols = set(target_cols.keys()) - set(stg_cols.keys())
       for new_col in new_cols:
           self.add_column(new_col, target_cols[new_col])

   def overwrite_target_table(self, col_definition, cols):

       swap_table = f"swap_{self.target_table}"
       temp_table = f"temp_{self.target_table}"

       self.drop_table(swap_table)
       self.create_table(col_definition, swap_table)
       self.copy_from_stage(cols, swap_table)
       self.drop_table(temp_table)
       self.swap_table(self.target_table, swap_table, temp_table)

   def swap_table(self, target: str, source: str, temp: str) -> str:
       result = self.cur.execute(f"ALTER TABLE {target} RENAME TO {temp};").fetchone()
       result1 = self.cur.execute(
           f"ALTER TABLE {source} RENAME TO {target};"
       ).fetchone()
       return {result, result1}

   def copy_from_stage(self, cols, tablename):

       statement = ""
       for col in cols:
           if col == "DWH_TIMESTAMP":
               statement += f'to_timestamp($1:"DWH_TIMESTAMP"::int, 9),'
           else:
               statement += f'$1:"{col}",'

       return self.cur.execute(
           f"""COPY INTO {tablename} FROM (SELECT {statement[:-1]} FROM @{self.target_stg_table})"""
       ).fetchone()

   def get_count(self, table=None) -> int:

       if table is None:
           table = self.target_table

       return self.cur.execute(
           f"SELECT COUNT(*) FROM {self.schema}.{table};"
       ).fetchone()[0]

   def get_max(self, column, table=None) -> int:

       if table is None:
           table = self.target_table

       return self.cur.execute(
           f"SELECT MAX({column}) FROM {self.schema}.{table};"
       ).fetchone()[0]

   def merge_table(self, cols, unique_columns):

       on = ",".join([f'TARGET."{col}" = SOURCE."{col}"' for col in unique_columns])
       update = ",".join([f'TARGET."{col}" = SOURCE."{col}"' for col in cols])
       columns = ",".join([f'"{col}"' for col in cols])
       values = ",".join([f'SOURCE."{col}"' for col in cols])

       stage_statement = ""
       for col in cols:
           if col == "DWH_TIMESTAMP":
               stage_statement += (
                   f'to_timestamp($1:"DWH_TIMESTAMP"::int, 9) AS "DWH_TIMESTAMP",'
               )
           else:
               stage_statement += f'$1:"{col}" AS "{col}",'

       stage_statement = f"SELECT {stage_statement[:-1]} FROM @{self.target_stg_table}"

       sql_statement = f"""
       MERGE INTO
           {self.schema}.{self.target_table} AS TARGET
       USING
           ({stage_statement}) AS SOURCE
       ON {on}
       WHEN MATCHED THEN
       UPDATE SET {update}
       WHEN NOT MATCHED THEN
       INSERT ({columns})
       VALUES ({values})
       """

       return self.cur.execute(sql_statement).fetchone()[0]


# In[3]:


from collections import namedtuple

ETLMode = {"full_refresh": "full_refresh", "incremental": "incremental"}

ETLMode = namedtuple("x", ETLMode.keys())(*ETLMode.values())


# # Uil

# In[4]:


import pandas as pd
from datetime import datetime
import os
from openpyxl import load_workbook
from collections import Counter

def source_to_parquet(
   tablename,
   filename,
   db_conn,
   etl_mode,
   path,
   sheet=None,
   skiprows=0,
   excel=False,
   offset=0,
):

   _file = os.path.join(path, filename)

   if excel == True:
       df = get_excel_df(_file,sheet,skiprows)       
   else:
       df = pd.read_csv(_file, skiprows=skiprows, dtype=str)

   if etl_mode != ETLMode.full_refresh:
       if df.shape[0] + offset < db_conn.get_count():
           raise Exception(
               f"DWH table:{tablename} has more count than source table:{filename}"
           )

   df.columns = [col.upper() for col in df.columns]
   df.insert(0, "ID", df.index.values + offset + 2 + skiprows)
   df["DWH_TIMESTAMP"] = datetime.now().replace(microsecond=0)

   df.dropna(how="all")

   df.to_parquet(
       path + f"{tablename}_parquet.gzip",
       compression="gzip",
       engine="fastparquet",
       index=False,
   )

   return get_col_def(df.columns), df.columns

def df_to_parquet(df, tablename, path = 'C:/import_snowflake/', offset = 0, skiprows = 0):

   df.columns = [col.upper() for col in df.columns]
   df.insert(0, "ID", df.index.values + offset + 2 + skiprows)
   df["DWH_TIMESTAMP"] = datetime.now().replace(microsecond=0)

   df.dropna(how="all")

   df.to_parquet(
       path + f"{tablename}_parquet.gzip",
       compression="gzip",
       engine="fastparquet",
       index=False,
   )

   return get_col_def(df.columns), df.columns

def get_col_def(cols):

   col_definition = ""
   for col in cols:
       if col == "DWH_TIMESTAMP":
           col_definition += f'"{col}" TIMESTAMP,'
       elif col == "ID":
           col_definition += f'"{col}" INT,'
       else:
           col_definition += f'"{col}" VARCHAR,'

   return col_definition[:-1]

def get_excel_df(_file,sheet,skiprows):
  
   wb = load_workbook(_file,read_only=True,data_only=True,keep_links=False)
   ws = wb[sheet]
   data = ws.values

   for _ in range(skiprows):
       next(data)

   cols = next(data)

   counter = dict(Counter(cols).items())
   for _key, _value in counter.items():
       counter[_key] = {'encounter':0,'cnt':_value}

   new_cols = []

   for col in cols:
       if counter[col]['encounter'] > 0:
           new_cols.append(f"{col}.{counter[col]['encounter']}")
       else:
           new_cols.append(col)

       counter[col]['encounter'] += 1

   df = pd.DataFrame(data,dtype=str,columns=new_cols)
   wb.close()
   df = df.loc[:,df.columns.values != None]
   df = df.loc[:,~df.columns.str.contains("None")]

   return df


# # csv Loader

# In[5]:


import sys

sys.path.append("..")
import argparse
import os
import logging


logging.basicConfig(level=logging.INFO)


def csv_upload__to_snowflake(schema, tablename, path, filename, mode):
  
   sf_loader = SnowflakeLoader(schema, tablename)
   print("====Connected to snowflake====")

   col_def, cols = source_to_parquet(
       tablename = tablename,
       filename = filename,
       db_conn = sf_loader,
       etl_mode = ETLMode.full_refresh, #incremental #full_refresh
       sheet=None,
       path= path,
       skiprows=0,
       excel=False,
       offset=0,
   )

   print(f"====Converted csv/excel {filename} to parquet====")

   try:
       print(1)
       sf_loader.create_table(col_def)
       print(2)
       sf_loader.create_stg_table()
       print(3)
       sf_loader.put_file(os.path.join(path, f"{tablename}_parquet.gzip"))
       print(4)

       if mode == ETLMode.full_refresh:
           print(5)
           sf_loader.overwrite_target_table(col_def, cols)
       elif mode == ETLMode.incremental:
           print(6)
           sf_loader.merge_table(cols, unique_key.split(","))
       print(f"====Loaded the {tablename} to DWH====")
   except Exception as e:
       logging.exception(e)
   finally:
       os.remove(path + f"{tablename}_parquet.gzip")
       sf_loader.close()



def csv_upload__to_snowflake__v2(schema, tablename, df, path, mode):
  
   sf_loader = SnowflakeLoader(schema, tablename)
   print("====Connected to snowflake====")

   col_def, cols = df_to_parquet(df, tablename)
   print(f"====df {tablename} to parquet====")

   try:
       print(1)
       sf_loader.create_table(col_def)
       print(2)
       sf_loader.create_stg_table()
       print(3)
       sf_loader.put_file(os.path.join(path, f"{tablename}_parquet.gzip"))
       print(4)

       if mode == ETLMode.full_refresh:
           print(5)
           sf_loader.overwrite_target_table(col_def, cols)
       elif mode == ETLMode.incremental:
           print(6)
           sf_loader.merge_table(cols, unique_key.split(","))
       print(f"====Loaded the {tablename} to DWH====")
   except Exception as e:
       logging.exception(e)
   finally:
       os.remove(path + f"{tablename}_parquet.gzip")
       sf_loader.close()

# In[6]:


# # CES UPDATE
# csv_upload__to_snowflake(
#       schema = 'PHUC'
#     , tablename = 'CES__test_importing'
#     , path = 'C:/import_snowflake/'
#     , filename = 'ces__feedback.csv'
#     , mode = ETLMode.full_refresh
# )



# # In[6]:


# # Operation

csv_upload__to_snowflake(
     schema = 'PHUC'
   , tablename = 'CES__OPERATION_METRIC'
   , path = 'C:/import_snowflake/'
   , filename = 'operation_metric.csv'
   , mode = ETLMode.full_refresh
)



