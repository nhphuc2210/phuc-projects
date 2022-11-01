# try:
import os,sys
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
import numpy as np
import time
import gspread
import platform
import re
from google.oauth2 import service_account
import google
# except Exception as e:
#     input("""
#     {}
#     Press any key to exit...""".format(e))


try:
    # prepare credntials
    # grant access view for account => userid@downloadsheet-277808.iam.gserviceaccount.com

    # location_file =  "/Users/c02c102plvdp/Google Drive/Shopee/Flash Sale Status version/crack.json"


    # location_file = 'C:/Crack/crack.json'
    
    location_file = 'cred/crack.json'

    gc = gspread.service_account(filename=location_file)
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(location_file, scopes=scopes)
    gc = gspread.authorize(credentials)

except Exception as e:
    input("""
    {}
    Press any key to exit...""".format(e))
    sys.exit()


def get_sheet_name(fileid):
    try:
        sheet_name = gc.open_by_key(fileid).worksheets()        
        return sheet_name
    except Exception as e:
        input("""
        {}
        Cannot get sheet_name""".format(e))

def get_data_from_gsheet(fileid, sheet_name, headline):
    try:
        df = pd.DataFrame(gc.open_by_key(fileid).worksheet(sheet_name).get_all_values())   
        new_df = df[headline:]
        new_header = df.iloc[headline-1]
        new_df.columns = new_header
        return new_df 
    except Exception as e:
        input("""
        {}
        Cannot get fileid = {}, sheet_name = {}""".format(e, fileid, sheet_name))
        sys.exit()

def upload_gsheet(your_dataframe, fileid, sheet_name):
    try:
        gc.open_by_key(fileid).worksheet(sheet_name).update([your_dataframe.columns.values.tolist()] + your_dataframe.values.tolist())        
    except Exception as e:
        input("""
        {}
        Cannot Upload""".format(e, fileid, sheet_name))
        sys.exit()

def delete_data(file_id,sheet_name,col_start='A',col_end='Z'):
    try:
        sh = gc.open_by_key(file_id)
        sh.values_clear(f"{sheet_name}!{col_start}:{col_end}")
    except Exception as e:
        input(f"""
        {e}
        Cannot Delete""")
        sys.exit()
