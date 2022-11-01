
# # Import Lib
 

 
import pandas as pd
import numpy as np
import time, sys, inspect, platform, os, pytz, datetime, io, shutil
from dateutil import tz
import warnings
from IPython.display import display
warnings.filterwarnings('ignore')
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzywuzzy import utils
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
license_hp_service = 'C:/cloud_service'
sys.path.append(license_hp_service)
from hoangphuc__snowflake_ingestion import csv_upload__to_snowflake__v2
import hoangphuc__snowflake_ingestion
contact = 'email: phucnguyen@synagie.com -phone number: 84937150860'
 

# # Build function
 

def get_header(data_frame, header_row):
    new_header = data_frame.iloc[header_row-1] #grab the first row for the header
    data_frame = data_frame[header_row:] #take the data less the header row
    data_frame.columns = new_header #set the header row as the df header
    return data_frame
 
def read_excel_w_header(file_source, sheet_name, header = None):
    start = datetime.datetime.now()
    data_frame = pd.read_excel(file_source, sheet_name)
    if header != None:
        new_header = data_frame.iloc[header-1] #grab the first row for the header
        data_frame = data_frame[header:] #take the data less the header row
        data_frame.columns = new_header #set the header row as the df header
    end = datetime.datetime.now()
    timing = end - start
    return data_frame, timing
 
def timestamp_now():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return now
 
def get_exactone(input_value, list_benchmark, threshold = 80):
    value = process.extractOne(input_value, list_benchmark, scorer=fuzz.ratio)[0]
    ratio = process.extractOne(input_value, list_benchmark, scorer=fuzz.ratio)[1]
    if ratio >= threshold:
        return value
 
def download_from_sharepoint(account_sharepoint, pwsd_sharepoint, site_url, file_name, file_path, download_to):
    try:
        ctx = ClientContext(site_url).with_credentials(UserCredential(account_sharepoint, pwsd_sharepoint))
        _file = open(download_to, "wb")
        ctx.web.get_file_by_server_relative_path(file_path).download(
                _file
            ).execute_query()
        print(f"====Downloaded Source File for {file_name}====")
        _file.close()
    except Exception as e:
        print(e)
        input("Cannot download. Press any key to exit.")
       
def ask__yes_no(mess):
    while True:
        answer = input('\n\t{} y/n: '.format(mess))
        if answer in ('y','n'):
            break
        else:
            print("\tInvalid input")
    return answer
 
def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
 
 
def del_file_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
 
 

# # Download file from sharepoint to get lastest updates
 

# create folder if not exist x remove old file
report_folder__ces = 'c:/bas_report/ces/'
create_folder_if_not_exists(report_folder__ces)
del_file_in_folder(report_folder__ces)
 
import_snowflake = 'C:/import_snowflake'
create_folder_if_not_exists(report_folder__ces)
 
 

 
# file source
 
all_brand_tracker = {
    "path": "/sites/synagie_pcs_regional/Shared Documents/PH - CES/Trackers/CES Tracker_All Brands.xlsm",
    "file_name": "all_brand.xlsm",
    "sheet_name" :  "CES Tracker",
    "header" : 2,
}
 
nike_tracker = {
    "path": "/sites/synagie_pcs_regional/Shared Documents/PH - CES/Trackers/CES Tracker_Nike.xlsm",
    "file_name": "nike.xlsm",
    "sheet_name" : "CES Tracker",
    "header" : 2,
}
 
vn_pr_tracker = {
    "path": "/sites/synagie_pcs_regional/Shared Documents/VN - CES/VN CES - Contact Form Daily update from 22 Mar 2021 - for CES Dashboard.xlsx",
    "file_name": "vn.xlsx",
    "sheet_name" : "Product Ratings and Reviews",
    "header" : 0,
 
}
 
vn_live_chat_tracker = {
    "path": "/sites/synagie_pcs_regional/Shared Documents/VN - CES/VN CES - Contact Form Daily update from 22 Mar 2021 - for CES Dashboard.xlsx",
    "file_name": "vn.xlsx",
    "sheet_name" : "Live Chats",
    "header" : 0,
 
}
 
 
sp_files = {
    all_brand_tracker["file_name"]: all_brand_tracker,
    nike_tracker["file_name"]: nike_tracker,
    vn_pr_tracker["file_name"]: vn_pr_tracker,
}
 
site_url = "https://avenzacorp.sharepoint.com/sites/synagie_pcs_regional/"
account_sharepoint = input("Pls input your company account ex. phucnguyen@synagie.com: ")
pwsd_sharepoint = input("Pls input your password: ")
 
 

answer = ask__yes_no("Do you want do re-download from sharepoint? ")
if answer == 'y':
   
    download_folder = 'c:/download_sharepoint/ces/'
    create_folder_if_not_exists(download_folder)    
    del_file_in_folder(download_folder)
 
    for file_name in (sp_files):
        print(f'{file_name} is downloading...')
        download_to = os.path.join(download_folder, file_name)
        file_path = sp_files[file_name]['path']
        download_from_sharepoint(account_sharepoint, pwsd_sharepoint, site_url, file_name, file_path, download_to)
 
 
 

# # Import file source
 

try:
    start_total = datetime.datetime.now()
    print(f'\nStart time: {start_total}')
 
    read_files = {
        'allbrand':all_brand_tracker,
        'nike':nike_tracker,
        'vn product x rating':vn_pr_tracker,
        'vn live chats':vn_live_chat_tracker,
    }
 
    for get_info in (read_files):
        re_read = 0
        while re_read <3 :
            try:
                file_name = read_files[get_info]['file_name']
                path_to_read = download_folder + file_name
                get_sheet = read_files[get_info]['sheet_name']
                header = read_files[get_info]['header']
                file_name__x__sheetname = f"File {file_name} - sheet {get_sheet}"
            #     print(file_name__x__sheetname)
 
                if file_name__x__sheetname == 'File all_brand.xlsm - sheet CES Tracker':
                    print(f'\nFile "{file_name}" - sheet "{get_sheet}" is loading...')
                    sharepoint_all_brand_2, timing = read_excel_w_header(path_to_read, get_sheet, header)
                    print(f'Reading Time: {timing}, data shape {sharepoint_all_brand_2.shape}')
                    break
                elif file_name__x__sheetname == 'File nike.xlsm - sheet CES Tracker':
                    print(f'\nFile "{file_name}" - sheet "{get_sheet}" is loading...')
                    nike_2, timing = read_excel_w_header(path_to_read, get_sheet, header)
                    print(f'Reading Time: {timing}, data shape {nike_2.shape}')
                    break
                if file_name__x__sheetname == 'File vn.xlsx - sheet Product Ratings and Reviews':
                    print(f'\nFile "{file_name}" - sheet "{get_sheet}" is loading...')
                    vn_product_review_2, timing = read_excel_w_header(path_to_read, get_sheet)
                    print(f'Reading Time: {timing}, data shape {vn_product_review_2.shape}')
                    break
                if file_name__x__sheetname == 'File vn.xlsx - sheet Live Chats':
                    print(f'\nFile "{file_name}" - sheet "{get_sheet}" is loading...')
                    vn_live_chat_2, timing = read_excel_w_header(path_to_read, get_sheet)
                    print(f'Reading Time: {timing}, data shape {vn_live_chat_2.shape}')
                    break  
            except Exception as e:
                re_read += 1
                print(f"\nTry to re-read {file_name}, {re_read} - due to {e}")
                time.sleep(3)
    end_total = datetime.datetime.now()
    print(f'\nEnd time: {end_total}')
    print(f'Total time to read: {end_total - start_total}')
except Exception as e:
    print(e)
    input("New errors was detected, press any key to exits")
    sys.exit()
 

# # SELECT same columns from 4 Source
 

# get new key
try:
    nike_3 = nike_2.loc[:, ['Name']]
    nike_3['Region'] = nike_2['Region']
    nike_3['Channel'] = nike_2['Channel']
    nike_3['Brand'] = nike_2['Brand']
    nike_3['Touchpoint'] = nike_2['Touchpoint']
    nike_3['Order Number'] = nike_2['Order Number']
    nike_3['Complaints'] = nike_2['Complaints']
    nike_3['Inquiry'] = nike_2['Inquiry']
    nike_3['Request'] = nike_2['Request']
    nike_3['Positive Comments'] = nike_2['Positive Comments']
    nike_3['Ratings'] = nike_2['Ratings']
    nike_3['Customer Message'] = nike_2['Customer Message']
    nike_3['CES Response'] = nike_2['CES Response']
    nike_3['Date Posted'] = nike_2['Date Posted']
    nike_3['Date Responded'] = nike_2['Date Responded']
    nike_3['Resolved'] = nike_2['Resolved']
    nike_3['Customer Name'] = nike_2.iloc[ : , 17]
    nike_3['Product'] = nike_2['Product']
    nike_3['Start of Day Count'] = nike_2['Start of Day Count']
    nike_3['End Of Day Count'] = nike_2['End Of Day Count']
    nike_3['Positive Seller Rating'] = nike_2['Positive Seller Rating']
    nike_3['Content Score'] = nike_2['Content Score']
    nike_3['Same-day Chat Response Rate'] = nike_2['Same-day Chat Response Rate']
    nike_3['Chat Response Time'] = nike_2['Chat Response Time']
    nike_3['Ship-on-Time (SOT)'] = nike_2['Ship-on-Time (SOT)']
    nike_3['Cancellation Rate'] = nike_2['Cancellation Rate']
    nike_3['Return Rate'] = nike_2['Return Rate']
    nike_3['Conversion Rate'] = nike_2['Conversion Rate']
    nike_3['Conversations'] = nike_2['Conversations']
    nike_3['Product Ratings Cleared?'] = nike_2['Product Ratings Cleared?']
    nike_3['Seller Ratings Cleared?'] = nike_2['Seller Ratings Cleared?']
    nike_3['Message Center Cleared?'] = nike_2['Message Center Cleared?']
    nike_3['Feed Link'] = nike_2['Feed Link']
    nike_3['Timestamp'] = nike_2['Timestamp']
    nike_3['Date'] = ''
    nike_3['Ticket #'] = ''
    nike_3['To'] = ''
    nike_3['CC'] = ''
    nike_3['Customer Name 2'] = ''
    nike_3['Email'] = ''
    nike_3['Ticket Status'] = ''
    nike_3['Email Resolution Date'] = ''
    nike_3['Merchant ID'] = ''
    nike_3['Store Name'] = ''
 
    nike__final = nike_3.loc[~nike_3['Timestamp'].isna(), :]
    nike__final['source'] = 'Nike'
    nike__final.shape
    print(f"Nike file has {nike__final.shape} rows ")
except Exception as e:
    print(e)
    input(f'\nAny column from file Nike was changed, pls update your app.{e}')
    sys.exit()
   
 

 
# get new key
try:
    vn_live_chat_3 = vn_live_chat_2.loc[:, ['Name']]
    vn_live_chat_3['Region'] = vn_live_chat_2['Region']
    vn_live_chat_3['Channel'] = vn_live_chat_2['Channel']
    vn_live_chat_3['Brand'] = vn_live_chat_2['Brand']
    vn_live_chat_3['Touchpoint'] = 'Live Chats'
    vn_live_chat_3['Order Number'] = vn_live_chat_2['Order Number']
    vn_live_chat_3['Complaints'] = vn_live_chat_2['Complaints']
    vn_live_chat_3['Inquiry'] = vn_live_chat_2['Inquiry']
    vn_live_chat_3['Request'] = vn_live_chat_2['Request']
    vn_live_chat_3['Positive Comments'] = vn_live_chat_2['Positive Comments']
    vn_live_chat_3['Ratings'] = ''
    vn_live_chat_3['Customer Message'] = ''
    vn_live_chat_3['CES Response'] = ''
    vn_live_chat_3['Date Posted'] = ''
    vn_live_chat_3['Date Responded'] = ''
    vn_live_chat_3['Resolved'] = ''
    vn_live_chat_3['Customer Name'] = ''
    vn_live_chat_3['Product'] = ''
    vn_live_chat_3['Start of Day Count'] = ''
    vn_live_chat_3['End Of Day Count'] = ''
    vn_live_chat_3['Positive Seller Rating'] = ''
    vn_live_chat_3['Content Score'] = ''
    vn_live_chat_3['Same-day Chat Response Rate'] = ''
    vn_live_chat_3['Chat Response Time'] = ''
    vn_live_chat_3['Ship-on-Time (SOT)'] = ''
    vn_live_chat_3['Cancellation Rate'] = ''
    vn_live_chat_3['Return Rate'] = ''
    vn_live_chat_3['Conversion Rate'] = ''
    vn_live_chat_3['Conversations'] = ''
    vn_live_chat_3['Product Ratings Cleared?'] = ''
    vn_live_chat_3['Seller Ratings Cleared?'] = ''
    vn_live_chat_3['Message Center Cleared?'] = ''
    vn_live_chat_3['Feed Link'] = ''
    vn_live_chat_3['Timestamp'] = vn_live_chat_2['Date & Hour (mm/dd/yyyy hh:mm)']
    vn_live_chat_3['Date'] = ''
    vn_live_chat_3['Ticket #'] = ''
    vn_live_chat_3['To'] = ''
    vn_live_chat_3['CC'] = ''
    vn_live_chat_3['Customer Name 2'] = ''
    vn_live_chat_3['Email'] = ''
    vn_live_chat_3['Ticket Status'] = ''
    vn_live_chat_3['Email Resolution Date'] = ''
    vn_live_chat_3['Merchant ID'] = ''
    vn_live_chat_3['Store Name'] = ''
 
 
    vn_livechat__final = vn_live_chat_3.loc[~vn_live_chat_3['Timestamp'].isna() , :]
    vn_livechat__final['source'] = 'VN Live Chats'
    vn_livechat__final.shape
    print(f"VN Live Chats has {vn_livechat__final.shape} rows ")
except Exception as e:
    print(e)
    input(f'\nAny column from file VN Live Chats was changed, pls update your app. {e}')
    sys.exit()
 

try:
    # get new key
    vn_product_review_3 = vn_product_review_2.loc[:, ['Name']]
    vn_product_review_3['Region'] = vn_product_review_2['Region']
    vn_product_review_3['Channel'] = vn_product_review_2['Channel']
    vn_product_review_3['Brand'] = vn_product_review_2['Brand']
    vn_product_review_3['Touchpoint'] = 'Product Ratings and Reviews'
    vn_product_review_3['Order Number'] = vn_product_review_2['Order Number']
    vn_product_review_3['Complaints'] = vn_product_review_2['Product RR - Complaints']
    vn_product_review_3['Inquiry'] = vn_product_review_2['Product RR - Inquiry']
    vn_product_review_3['Request'] = vn_product_review_2['Product RR - Request']
    vn_product_review_3['Positive Comments'] = vn_product_review_2['Product RR - Positive Comments']
    vn_product_review_3['Ratings'] = vn_product_review_2['Rating']
    vn_product_review_3['Customer Message'] = vn_product_review_2['Customer Review']
    vn_product_review_3['CES Response'] = vn_product_review_2['CES Response']
    vn_product_review_3['Date Posted'] = vn_product_review_2['Date Posted']
    vn_product_review_3['Date Responded'] = vn_product_review_2['Date Responded']
    vn_product_review_3['Resolved'] = vn_product_review_2['Resolved']
    vn_product_review_3['Customer Name'] = ''
    vn_product_review_3['Product'] = ''
    vn_product_review_3['Start of Day Count'] = ''
    vn_product_review_3['End Of Day Count'] = ''
    vn_product_review_3['Positive Seller Rating'] = ''
    vn_product_review_3['Content Score'] = ''
    vn_product_review_3['Same-day Chat Response Rate'] = ''
    vn_product_review_3['Chat Response Time'] = ''
    vn_product_review_3['Ship-on-Time (SOT)'] = ''
    vn_product_review_3['Cancellation Rate'] = ''
    vn_product_review_3['Return Rate'] = ''
    vn_product_review_3['Conversion Rate'] = ''
    vn_product_review_3['Conversations'] = ''
    vn_product_review_3['Product Ratings Cleared?'] = ''
    vn_product_review_3['Seller Ratings Cleared?'] = ''
    vn_product_review_3['Message Center Cleared?'] = ''
    vn_product_review_3['Feed Link'] = ''
    vn_product_review_3['Timestamp'] = vn_product_review_2['Date & Hour (mm/dd/yyyy hh:mm)']
    vn_product_review_3['Date'] = ''
    vn_product_review_3['Ticket #'] = ''
    vn_product_review_3['To'] = ''
    vn_product_review_3['CC'] = ''
    vn_product_review_3['Customer Name 2'] = ''
    vn_product_review_3['Email'] = ''
    vn_product_review_3['Ticket Status'] = ''
    vn_product_review_3['Email Resolution Date'] = ''
    vn_product_review_3['Merchant ID'] = ''
    vn_product_review_3['Store Name'] = ''
 
 
    vn_product__final = vn_product_review_3.loc[~vn_product_review_3['Timestamp'].isna(), :]
    vn_product__final['source'] = 'VN Product Ratings and Reviews'
    vn_product__final.shape
    print(f"VN Product Rating has {vn_product__final.shape} rows ")
except Exception as e:
    print(e)
    input(f'\nAny column from file VN Product x Review was changed, pls update your app. {e}')
    sys.exit()
 
 

try:
    # get new key
    sharepoint_all_brand_3 = sharepoint_all_brand_2.loc[:, ['Name']]
    sharepoint_all_brand_3['Region'] = sharepoint_all_brand_2['Region']
    sharepoint_all_brand_3['Channel'] = sharepoint_all_brand_2['Channel']
    sharepoint_all_brand_3['Brand'] = sharepoint_all_brand_2['Brand']
    sharepoint_all_brand_3['Touchpoint'] = sharepoint_all_brand_2['Touchpoint']
    sharepoint_all_brand_3['Order Number'] = sharepoint_all_brand_2['Order Number']
    sharepoint_all_brand_3['Complaints'] = sharepoint_all_brand_2['Complaints']
    sharepoint_all_brand_3['Inquiry'] = sharepoint_all_brand_2['Inquiry']
    sharepoint_all_brand_3['Request'] = sharepoint_all_brand_2['Request']
    sharepoint_all_brand_3['Positive Comments'] = sharepoint_all_brand_2['Positive Comments']
    sharepoint_all_brand_3['Ratings'] = sharepoint_all_brand_2['Ratings']
    sharepoint_all_brand_3['Customer Message'] = sharepoint_all_brand_2['Customer Message']
    sharepoint_all_brand_3['CES Response'] = sharepoint_all_brand_2['CES Response']
    sharepoint_all_brand_3['Date Posted'] = sharepoint_all_brand_2['Date Posted']
    sharepoint_all_brand_3['Date Responded'] = sharepoint_all_brand_2['Date Responded']
    sharepoint_all_brand_3['Resolved'] = sharepoint_all_brand_2['Resolved']
    sharepoint_all_brand_3['Customer Name'] = sharepoint_all_brand_2.iloc[:, 16]
    sharepoint_all_brand_3['Product'] = sharepoint_all_brand_2['Product']
    sharepoint_all_brand_3['Start of Day Count'] = sharepoint_all_brand_2['Start of Day Count']
    sharepoint_all_brand_3['End Of Day Count'] = sharepoint_all_brand_2['End Of Day Count']
    sharepoint_all_brand_3['Positive Seller Rating'] = sharepoint_all_brand_2['Positive Seller Rating']
    sharepoint_all_brand_3['Content Score'] = sharepoint_all_brand_2['Content Score']
    sharepoint_all_brand_3['Same-day Chat Response Rate'] = sharepoint_all_brand_2['Same-day Chat Response Rate']
    sharepoint_all_brand_3['Chat Response Time'] = sharepoint_all_brand_2['Chat Response Time']
    sharepoint_all_brand_3['Ship-on-Time (SOT)'] = sharepoint_all_brand_2['Ship-on-Time (SOT)']
    sharepoint_all_brand_3['Cancellation Rate'] = sharepoint_all_brand_2['Cancellation Rate']
    sharepoint_all_brand_3['Return Rate'] = sharepoint_all_brand_2['Return Rate']
    sharepoint_all_brand_3['Conversion Rate'] = sharepoint_all_brand_2['Conversion Rate']
    sharepoint_all_brand_3['Conversations'] = sharepoint_all_brand_2['Conversations']
    sharepoint_all_brand_3['Product Ratings Cleared?'] = sharepoint_all_brand_2['Product Ratings Cleared?']
    sharepoint_all_brand_3['Seller Ratings Cleared?'] = sharepoint_all_brand_2['Seller Ratings Cleared?']
    sharepoint_all_brand_3['Message Center Cleared?'] = sharepoint_all_brand_2['Message Center Cleared?']
    sharepoint_all_brand_3['Feed Link'] = sharepoint_all_brand_2['Feed Link']
    sharepoint_all_brand_3['Timestamp'] = sharepoint_all_brand_2['Timestamp']
    sharepoint_all_brand_3['Date'] = ''
    sharepoint_all_brand_3['Ticket #'] = sharepoint_all_brand_2['Ticket #']
    sharepoint_all_brand_3['To'] = sharepoint_all_brand_2['To']
    sharepoint_all_brand_3['CC'] = sharepoint_all_brand_2['CC']
    sharepoint_all_brand_3['Customer Name 2'] = sharepoint_all_brand_2.iloc[:, 39]
    sharepoint_all_brand_3['Email'] = sharepoint_all_brand_2['Email']
    sharepoint_all_brand_3['Ticket Status'] = sharepoint_all_brand_2['Ticket Status']
    sharepoint_all_brand_3['Email Resolution Date'] = sharepoint_all_brand_2['Email Resolution Date']
    sharepoint_all_brand_3['Merchant ID'] = ''
    sharepoint_all_brand_3['Store Name'] = ''
 
 
    sharepoint__final = sharepoint_all_brand_3.loc[~sharepoint_all_brand_3['Timestamp'].isna() , :]
    sharepoint__final['source'] = 'All Brand'
    sharepoint__final.shape
    print(f"All Brand has {sharepoint__final.shape} rows ")
except Exception as e:
    print(e)
    input(f'\nAny column from file All Brand was changed, pls update your app. {e}')
    sys.exit()
 
 

# gg__2 = google_source.loc[:, ['Name']]
 
# # get new key
# gg__2 = google_source.loc[:, ['Name']]
# gg__2['Region'] = np.where( google_source['Region'] == 'Singapore', 'SG',
#                            np.where( google_source['Region'] == 'Philippines', 'PH',
#                                    np.where( google_source['Region'] == 'Malaysia', 'MY',
#                                            np.where( google_source['Region'] == 'Thailand', 'TH',
#                                                     np.where( google_source['Region'] == 'Indonesia', 'ID',
#                                                              np.where( google_source['Region'] == 'Vietnam', 'VN',''
#                                                 ))))))
# gg__2['Channel'] = np.where( google_source['Region'] == 'Singapore', google_source['Channels -SG'],
#                            np.where( google_source['Region'] == 'Philippines', google_source['Channels - PH'],
#                                    np.where( google_source['Region'] == 'Malaysia', google_source['Channels - MY'],
#                                            np.where( google_source['Region'] == 'Thailand', google_source['Channels -TH'],
#                                                     np.where( google_source['Region'] == 'Indonesia', google_source['Channels - ID'],
#                                                              np.where( google_source['Region'] == 'Vietnam', google_source['Channels -VN'],''
#                                                 ))))))
 
# gg__2['Brand'] =  np.where( google_source['Region'] == 'Singapore', google_source['Brand/Sellers - SG'],
#                            np.where( google_source['Region'] == 'Philippines', google_source['Brand/Sellers - PH'],
#                                    np.where( google_source['Region'] == 'Malaysia', google_source['Brand/Sellers - MY'],
#                                            np.where( google_source['Region'] == 'Thailand', google_source['Brand/Sellers - TH'],
#                                                     np.where( google_source['Region'] == 'Indonesia', google_source['Brand/Sellers - ID'],
#                                                              np.where( google_source['Region'] == 'Vietnam', google_source['Brand/Sellers - VN'],''
#                                                 ))))))
 
# gg__2['Touchpoint'] = np.where( google_source['Region'] == 'Singapore', google_source['Touchpoints - SG'],
#                            np.where( google_source['Region'] == 'Philippines', google_source['Touchpoints - PH'],
#                                    np.where( google_source['Region'] == 'Malaysia', google_source['Touchpoints - MY'],
#                                            np.where( google_source['Region'] == 'Thailand', google_source['Touchpoints - TH'],
#                                                     np.where( google_source['Region'] == 'Indonesia', google_source['Touchpoints - ID'],
#                                                              np.where( google_source['Region'] == 'Vietnam', google_source['Touchpoints - VN'],''
#                                                 ))))))
 
# gg__2['Order Number'] = google_source['Order number'] + google_source['Order number.1'] + google_source['Order number.2']
# gg__2['Complaints'] = google_source['Chat - Complaints'] + google_source['Product RR - Complaints'] + google_source['Seller RR - Complaints'] +google_source['Complaints'] +google_source['Complaints.1'] + google_source['Complaints.2'] + google_source['Complaints.3'] + google_source['Complaints.4'] + google_source['Complaints.5']
# gg__2['Inquiry'] = google_source['Chat - Inquiry'] + google_source['Product RR - Inquiry'] + google_source['Seller RR - Inquiry'] + google_source['Inquiry'] + google_source['Inquiry.1'] + google_source['Inquiry.2'] + google_source['Inquiry.3'] + google_source['Inquiry.4'] + google_source['Inquiry.5']
# gg__2['Request'] = google_source['Chat - Request']+google_source['Product RR - Request']+google_source['Seller RR - Request']+google_source['Request']+google_source['Request.1']+google_source['Request.2']+google_source['Request.3']+google_source['Request.4']+google_source['Request.5']
# gg__2['Positive Comments'] = google_source['Chat - Positive Comments']+google_source['Product RR - Positive Comments']+google_source['Seller RR - Positive Comments']+google_source['Positive Comments']+google_source['Positive Comments.1']+google_source['Positive Comments.2']+google_source['Positive Comments.3']+google_source['Positive Comments.4']+google_source['Positive Comments.5']
# gg__2['Ratings'] = google_source['Ratings']+ google_source['Seller RR - Ratings']
# gg__2['Customer Message'] = google_source['Customer message']
# gg__2['CES Response'] = google_source['CES Response']+google_source['CES Response.1']
# gg__2['Date Posted'] = google_source['Date Posted'] + google_source['Date Posted.1'] + google_source['Date Posted.2']
# gg__2['Date Responded'] = google_source['Date Responded']+ google_source['Date Responded.1'] + google_source['Date Responded.2']
# gg__2['Resolved'] = google_source['Resolved']+google_source['Resolved.1']
# gg__2['Customer Name'] = google_source['Customer Name']
# gg__2['Product'] = google_source['Product']
# gg__2['Start of Day Count'] = google_source['Start of Day Count']
# gg__2['End Of Day Count'] = google_source['End of Day Count']
# gg__2['Positive Seller Rating'] = google_source['Positive Seller Rating']
# gg__2['Content Score'] = google_source['Content Score']
# gg__2['Same-day Chat Response Rate'] = google_source['Same-day Chat Response Rate']
# gg__2['Chat Response Time'] = google_source['Chat Response Time']
# gg__2['Ship-on-Time (SOT)'] = google_source['Ship-on-Time (SOT)']
# gg__2['Cancellation Rate'] = google_source['Cancellation Rate']
# gg__2['Return Rate'] = google_source['Return Rate']
# gg__2['Conversion Rate'] = google_source['Conversion Rate']
# gg__2['Conversations'] = google_source['Conversations']
# gg__2['Product Ratings Cleared?'] = google_source['Product Ratings Cleared? ']
# gg__2['Seller Ratings Cleared?'] = google_source['Seller Ratings Cleared? ']
# gg__2['Message Center Cleared?'] = google_source['Message Center Cleared? ']
# gg__2['Feed Link'] = ''
# gg__2['Timestamp'] = google_source['Timestamp']
# gg__2['Date'] = ''
# gg__2['Ticket #'] = ''
# gg__2['To'] = ''
# gg__2['CC'] = ''
# gg__2['Customer Name 2'] = ''
# gg__2['Email'] = ''
# gg__2['Ticket Status'] = ''
# gg__2['Email Resolution Date'] = ''
# gg__2['Merchant ID'] = ''
# gg__2['Store Name'] = ''
 
 
# gg__final = gg__2.loc[ ~gg__2['Timestamp'].isna() , :]
# gg__final['source'] = 'Google form'
# gg__final.shape
 

# # UNION ALL SOURCE
 

try:
    print(f"\nUnion all file...")
    ces__feedback = nike__final.append([sharepoint__final,vn_product__final,vn_livechat__final]).reset_index(drop = True)
except Exception as e:
    print(e)
    input("Some file cannot read. Press any key to exits")
    sys.exit()
   
print(f"CES__FEEDBACK: {ces__feedback.shape} - Before cleanup ")
 

# # Clean up columns
 

# # Download master files
 

mapping_masterfile = os.path.join(download_folder, "mapping__master_file.xlsx")
mapping_masterfile
 

re_download = 0
while re_download < 3:
    try:
        print(f"\nMaster file is downloading...")
        download_from_sharepoint(account_sharepoint, pwsd_sharepoint
                                , site_url = "https://avenzacorp.sharepoint.com/sites/BAS/"
                                , file_name = "mapping__master_file.xlsx"
                                , file_path = """/sites/BAS/Shared Documents/3.CES/mapping__master_file.xlsx"""
                                , download_to = mapping_masterfile
                                )
        break
    except Exception as e:
        re_download +=1
        print(f"\nTry to re-download due to {e}")
        time.sleep(3)
 

# ## Region Clean up
 

try:
    print(f"\nColumn Region is being cleaned...")
    url_mapping = 'https://avenzacorp.sharepoint.com/:x:/r/sites/BAS/_layouts/15/Doc.aspx?sourcedoc=%7BE499B6E7-A7B8-4708-9360-E1EA93170D0D%7D&file=mapping__master_file.xlsx&action=default&mobileredirect=true'
    region__orginal = pd.read_excel(mapping_masterfile, sheet_name = 'region')
    region__orginal
 
    ces__feedback['Region'] = ces__feedback['Region'].str.rstrip('.!? \n\t')
 
    before = ces__feedback.shape[0]
    ces__feedback__2 = pd.merge(
                                        ces__feedback,
                                        region__orginal,
                                        how="left",
                                        on=None,
                                        left_on='Region',
                                        right_on='region__mapping',
                                        left_index=False,right_index=False,sort=True,suffixes=("before_", "after_"),copy=True,indicator=False,validate=None,
                                    )
    # check mapping
    after = ces__feedback__2.shape[0]
    if after != before:
        input("Duplicated in mapping file {}, need to remove duplicate first, sheet region".format(url_mapping))
 
    # check clean up    
    region_report = ces__feedback__2.loc[ (ces__feedback__2['region__mapping'].isna()) & (~ces__feedback__2['Region'].isna())
                                              , ['source','Name','Timestamp','Region', 'region__mapping'] ].drop_duplicates()
 
    # remove invalid region
    ces__feedback__2 = ces__feedback__2.loc[ ~ces__feedback__2['region__cleaned'].isna() , :]
 
    if len(region_report) > 0:
        display(region_report)
    else:
        print("Done - Region is cleaned")
except Exception as e:
    print(e)
    input('Cannot clean up Region. Press any key to exit...')
    sys.exit()
 
 
 

# ## Touchpoint Clean up
 

try:
    print(f"\nColumn Touchpoint is being cleaned...")
    touchpoint_mapping = pd.read_excel(mapping_masterfile, sheet_name = 'touch_point')
 
    before = ces__feedback__2.shape[0]
    ces__feedback__3 = pd.merge(
                                        ces__feedback__2,
                                        touchpoint_mapping,
                                        how="left",
                                        on=None,
                                        left_on='Touchpoint',
                                        right_on='touchpoint__mapping',
                                        left_index=False,right_index=False,sort=True,suffixes=("before_", "after_"),copy=True,indicator=False,validate=None,
                                    )
    after = ces__feedback__3.shape[0]
    if after != before:
        input("Duplicated in mapping file {}, need to remove duplicate first, sheet region".format(url_mapping))
 
 
    # check clean up    
    touchpoint_report = ces__feedback__3.loc[ (ces__feedback__3['touchpoint__cleanned'] == '') & (~ces__feedback__3['Touchpoint'].isna())
                                              , ['source','Name','Touchpoint', 'touchpoint__cleanned'] ].drop_duplicates()
 
    if len(touchpoint_report) > 0:
        display(touchpoint_report)
    else:
        print("Done - Touchpoint is cleaned")
except Exception as e:
    print(e)
    input('Cannot clean up Touchpoint. Press any key to exit...')
    sys.exit()    
 

# ## Date Clean up
 

try:
    print(f"\nColumn Date is being cleaned...")
    ces__feedback__date_clean = ces__feedback__3
 
    # convert to string
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].astype(str)
 
    # replace invalid character
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("'","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("\\","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("//","/")                                                                                            
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("]","")                                                                                            
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("  "," ")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(": ",":")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(";",":")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(".",":")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("::",":")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("h",":")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace("_x0008_","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(" AM","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(" PM","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(":PM","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(" SA","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(" CH","")
    ces__feedback__date_clean['Timestamp'] = ces__feedback__date_clean['Timestamp'].str.replace(" GMT\+7","")
 
 
 
    # convert to date
 
    ces__feedback__date_clean['date_type_1'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%Y-%m-%d', errors = 'coerce')
    ces__feedback__date_clean['date_type_11'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%Y/%m/%d %H:%M:%S', errors = 'coerce')
    ces__feedback__date_clean['date_type_10'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%Y-%m-%d %H:%M:%S:%f', errors = 'coerce')
    ces__feedback__date_clean['date_type_2'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%Y-%d-%m', errors = 'coerce')
    ces__feedback__date_clean['date_type_3'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%d/%m/%Y', errors = 'coerce')
    ces__feedback__date_clean['date_type_4'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%m/%d/%Y', errors = 'coerce')
    ces__feedback__date_clean['date_type_5'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%m/%d/%y %H:%M', errors = 'coerce')
    ces__feedback__date_clean['date_type_6'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%m/%d/%Y %H:%M', errors = 'coerce')
    ces__feedback__date_clean['date_type_7'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%d/%m/%Y %H:%M', errors = 'coerce')
    ces__feedback__date_clean['date_type_8'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%m/%d/%Y %H:%M:%S', errors = 'coerce')
    ces__feedback__date_clean['date_type_9'] = pd.to_datetime(ces__feedback__date_clean['Timestamp'] , format = '%d/%m/%Y %H:%M:%S', errors = 'coerce')
 
 
    ces__feedback__date_clean['Date'] = ces__feedback__date_clean['date_type_1']\
                                .fillna(ces__feedback__date_clean['date_type_4'])\
                                .fillna(ces__feedback__date_clean['date_type_3'])\
                                .fillna(ces__feedback__date_clean['date_type_2'])\
                                .fillna(ces__feedback__date_clean['date_type_5'])\
                                .fillna(ces__feedback__date_clean['date_type_6'])\
                                .fillna(ces__feedback__date_clean['date_type_7'])\
                                .fillna(ces__feedback__date_clean['date_type_8'])\
                                .fillna(ces__feedback__date_clean['date_type_9'])\
                                .fillna(ces__feedback__date_clean['date_type_10'])\
                                .fillna(ces__feedback__date_clean['date_type_11'])
 
    # ces__feedback__date_clean.loc[ ces__feedback__date_clean['Order Number'] == '210906HJD4PYDD' , ['Timestamp','date_type_1','date_type_2','date_type_3','date_type_4','date_type_5','date_type_6','date_type_7','date_type_8','Date'] ]
 
    invalid_date = ces__feedback__date_clean['Date'] >= (pd.Timestamp.today() + pd.DateOffset(1))
 
    # change invalid date
    ces__feedback__date_clean.loc[ invalid_date , 'Date' ] = pd.to_datetime( ces__feedback__date_clean.loc[ invalid_date , 'Date' ].dt.strftime('%Y-%d-%m'), format = '%Y-%m-%d', errors = 'coerce')
 
    # export data report
    invalid_date_2 = (ces__feedback__date_clean['Date'] >= (pd.Timestamp.today() + pd.DateOffset(1)) ) | ces__feedback__date_clean['Date'].isna()
 
    date_report = ces__feedback__date_clean.loc[ invalid_date_2 , ['source','Name', 'Region', 'Channel', 'Order Number','Timestamp', 'Date' ] ].reset_index(drop = True)
 
    display(date_report)
 
    # remove invalid date
    ces__feedback__4 = ces__feedback__date_clean.loc[ ~invalid_date_2 , :]
    ces__feedback__4.shape
except Exception as e:
    print(e)
    input('Cannot clean up Date. Press any key to exit...')
    sys.exit()
 

# ## Store Name Mapping
 

# 1. Brand to store_name__input and merchant_id__input
# 2. store_name__cleaned_by_merchant_id = mapping merchant_id w s3 source
# 3. store_name__cleaned_by_previous_storename mapping = mapping w store name mapping source
# 4. store_name__cleaned_by_detected = detect by s3 source
# 5. export detect store name to report
# 6. merge all store name cleaned x remove invalid store name
#
 

# get s3 files mapping
try:
    print(f"\nColumn Store Name is being cleaned by Merchant ID inputed...")
    master_list = pd.read_excel(mapping_masterfile, sheet_name = 'master_list')
    get_masterlist = master_list.loc[ : , ['merchant_id', 'store_name'] ].drop_duplicates()
 
    # Split Store Name Input > merchant_id input
    ces__feedback__4['store_name__input'] = ces__feedback__4['Brand'].astype(str).str.split("|", expand=True)[0].astype(str).str.strip()
    ces__feedback__4['merchant_id__input'] = ces__feedback__4['Brand'].astype(str).str.split("|", expand=True)[1].astype(str).str.upper().str.strip()
 
    # store_name__cleaned by merchant_id input
    before = ces__feedback__4.shape[0]
    ces__feedback__by_merchant_id_input = pd.merge(
                                        ces__feedback__4,
                                        get_masterlist,
                                        how="left",
                                        on=None,
                                        left_on=['merchant_id__input'] ,
                                        right_on=['merchant_id'],
                                        left_index=False,right_index=False,sort=True,suffixes=("", "_cleaned__by_merchantid_input"),copy=True,indicator=False,validate=None,
                                    )
    # check mapping
    after = ces__feedback__by_merchant_id_input.shape[0]
    if after != before:
        print(f"Check duplicated. Before = {before}, after = {after}")
except Exception as e:
    input(f"\nCannot clean Store Name by Merchant ID inputed due to {e}. Press any key to exit...")
    sys.exit()
   
# cleaned store name = store_name <----
 

# previous mapping data
try:
    print(f"\nColumn Store Name is being cleaned by Store Name inputed...")
    store_name__orginal = pd.read_excel(mapping_masterfile, sheet_name = 'store_name')
    get_store_name__orginal = store_name__orginal.loc[:, ['store_name__input','store_name__cleaned']].drop_duplicates().reset_index(drop=True)
 
    # store_name__cleaned by merchant_id input
    before = ces__feedback__by_merchant_id_input.shape[0]
    ces__feedback__store_name_input = pd.merge(
                                        ces__feedback__by_merchant_id_input,
                                        get_store_name__orginal,
                                        how="left",
                                        on=None,
                                        left_on=['store_name__input'] ,
                                        right_on=['store_name__input'],
                                        left_index=False,right_index=False,sort=True,suffixes=("", "__by_store_name_input"),copy=True,indicator=False,validate=None,
                                    )
    # check mapping
    after = ces__feedback__store_name_input.shape[0]
    if after != before:
        print(f"Check duplicated. Before = {before}, after = {after}")
except Exception as e:
    input(f"\nCannot clean Store Name by Store Name inputed due to {e}. Press any key to exit...")
    sys.exit()
 
# cleaned store name =  store_name__cleaned <-------
 

try:
    print(f"\nColumn Store Name is being cleaned by detecting Store Name inputed...")
    # prepare data for
    ces__feedback__4_1 = ces__feedback__store_name_input.copy()
    ces__feedback__4_1['store_name__cleaned_merge'] = ces__feedback__4_1['store_name'].fillna(ces__feedback__4_1['store_name__cleaned'])
    ces__feedback__4_1['store_name__cleaned_merge']
 
    # get store name need to scan
    store_name__need_to_scan = ces__feedback__4_1.loc[ ces__feedback__4_1['store_name__cleaned_merge'].isna() , ['store_name__input'] ].drop_duplicates()
 
    # get data
    master_list = pd.read_excel(mapping_masterfile, sheet_name = 'master_list')
    store_name__valid = list(master_list['store_name'].unique())
 
    # scan storename
    store_name__need_to_scan['store_name__after_scan'] = store_name__need_to_scan['store_name__input'].fillna('').astype(str).apply(lambda x: get_exactone(input_value = x, list_benchmark = store_name__valid, threshold = 60))
 
    # merge store_name after scan
    before = ces__feedback__4_1.shape[0]
    ces__feedback__4_2 = pd.merge(
                                        ces__feedback__4_1,
                                        store_name__need_to_scan,
                                        how="left",
                                        on=None,
                                        left_on=['store_name__input'] ,
                                        right_on=['store_name__input'],
                                        left_index=False,right_index=False,sort=True,suffixes=("", "__scanned"),copy=True,indicator=False,validate=None,
                                    )
    after = ces__feedback__4_2.shape[0]
    if after != before:
        print(f"Check duplicated. Before = {before}, after = {after}")
 
    # final store name cleaned
    ces__feedback__4_2['store_name__final'] = ces__feedback__4_2['store_name__cleaned_merge'].fillna(ces__feedback__4_2['store_name__after_scan'])
 
except Exception as e:
    input(f"\nCannot clean Store Name by detecting Store Name inputed due to {e}. Press any key to exit...")
    sys.exit()
 
 

# # Export store name scanned to report
 

try_export = 0
while try_export <3 :
    try:
        mess = 'Export Store Name was in valid'
        print(f"\nTry {mess}...")
        # try to detect invalid input
        df_report__storename_need_to_add = ces__feedback__4_2.loc[ (~ces__feedback__4_2['store_name__after_scan'].isna()) , ['Brand','region__cleaned','store_name__after_scan'] ].drop_duplicates().reset_index(drop=True)
 
        # export df detected to .csv to paste sharepoint files
        df_report__storename_need_to_add.to_csv(os.path.join(report_folder__ces, 'brand_need_to_add.csv'), encoding='utf-8-sig', index=False)
        df_report__storename_need_to_add.head(5)
        break
    except Exception as e:
        try_export += 1
        input(f"\nCannot {mess} due to {e}. Try {try_export} after 5 sec.")
        time.sleep(5)
   
 
 

try:
    mess = 'Get Report Store Name Invalid'
    print(f"\nTry {mess}...")
    report_store_name_invalid = ces__feedback__4_2.loc[ (ces__feedback__4_2['store_name__final'].isna()) , ['source','Name','Brand','region__cleaned','store_name__final'] ].drop_duplicates().sort_values(by=['source']).reset_index(drop=True)
    report_store_name_invalid.head(5)
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Try {try_export} after 5 sec.")
    sys.exit()
 

 
 

# ## Clean up channel
 

try:
    mess = 'Get valid Channel'
    print(f"\nTry {mess}...")
 
    master_list = pd.read_excel(mapping_masterfile , sheet_name = 'master_list')
 
    valid_channel = pd.DataFrame( master_list.sort_values('channel').groupby(['merchant_id'])['channel'].apply(list) ).reset_index().rename_axis(None, axis=1)
 
    def get_channel(x):
        if 'Lazada' in x:
            return 'Lazada'
        elif 'Shopee' in x:
            return 'Shopee'
        else:
            return x[0]
 
    valid_channel['first_channel'] = valid_channel['channel'].apply(lambda x: get_channel(x))
 
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 

try:
    mess = 'Get Merchant ID by Store Name cleaned x Region Cleaned'
    print(f"\nTry {mess}...")
    master_list = pd.read_excel(mapping_masterfile , sheet_name = 'master_list')
    get_merchant_id__s3 = master_list.loc[: ,['region','store_name','merchant_id']].drop_duplicates().reset_index(drop=True)
 
    # get merchant_id by store name x region
    before = ces__feedback__4_2.shape[0]
    ces__feedback__5 = pd.merge(
                                        ces__feedback__4_2,
                                        get_merchant_id__s3,
                                        how="left",
                                        on=None,
                                        left_on=['store_name__final', 'region__cleaned'] ,
                                        right_on=['store_name','region'],
                                        left_index=False,right_index=False,sort=True,suffixes=("", "_get_merchantid"),copy=True,indicator=False,validate=None,
                                    )
    # check mapping
    after = ces__feedback__5.shape[0]
    if after != before:
        print(before, after)
        print(f"Check duplicated. Before = {before}, after = {after}")
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 

try:
    mess = 'Check Channnel'
    print(f"\nTry {mess}...")
    before = ces__feedback__5.shape[0]
    ces__feedback__7 = pd.merge(
                                        ces__feedback__5,
                                        valid_channel,
                                        how="left",
                                        on=None,
                                        left_on=['merchant_id_get_merchantid'] ,
                                        right_on=['merchant_id'],
                                        left_index=False,right_index=False,sort=True,suffixes=("_before", "_after"),copy=True,indicator=False,validate=None,
                                    )
    # check mapping
    after = ces__feedback__7.shape[0]
    if after != before:
        print(before, after)
        print("Duplicated in mapping file {}, need to remove duplicate first, sheet touch_point".format(url_mapping))
 
 
    ces__feedback__7.loc[ ces__feedback__7['channel'].isna() , 'channel' ] = 'MerchantID doesnt exist on S3 source'
 
    # check valid channel input
    ces__feedback__7['is_valid_channel'] = ces__feedback__7.apply(lambda x: True if str(x['Channel']) in x['channel'] else False,axis=1)
 
    # channel cleaned
    ces__feedback__7['channel__cleaned'] = ces__feedback__7['Channel']
    ces__feedback__7.loc[ ces__feedback__7.is_valid_channel == False, 'channel__cleaned' ] = ces__feedback__7.loc[ ces__feedback__7.is_valid_channel == False, 'first_channel']
 
    # remove invalid channel
    ces__feedback__8 = ces__feedback__7.loc[ ces__feedback__7['channel__cleaned'] != "MerchantID doesnt exist on S3 source" , : ]
 
    # export report invalid channel
    report__invalid_channel = ces__feedback__7.loc[ ces__feedback__7['channel__cleaned'] == "MerchantID doesnt exist on S3 source" , ['source','Brand','Channel','Name','Timestamp','channel','channel__cleaned'] ].drop_duplicates().reset_index(drop=True)
 
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 

# ## Clean metrics
 

try:
    mess = 'Clean up Metrics'
    print(f"\nTry {mess}...")
    columns_percentage_list = ['Positive Seller Rating','Same-day Chat Response Rate','Ship-on-Time (SOT)','Conversion Rate','Return Rate','Conversion Rate']
    for column in columns_percentage_list:
        print(column)
        # get number only - remove string
        ces__feedback__8[column] = ces__feedback__8[column].astype('str').str.extract(r'(\d+[.\d]*)')
        ces__feedback__8[column] = pd.to_numeric(ces__feedback__8[column], errors='coerce')
 
        # convert string to float
        ces__feedback__8[column] = ces__feedback__8[column].astype(float)
 
        # divide 100 if % > 100%
        ces__feedback__8.loc[ ces__feedback__8[column] > 1 , column ] = ces__feedback__8.loc[ ces__feedback__8[column] > 1 , column ]/100
 
        # if still > 1 then 1
        ces__feedback__8.loc[ ces__feedback__8[column] > 1 , column ] = 1
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 

try:
    # chat response time
    ces__feedback__8['Chat Response Time'] = ces__feedback__8['Chat Response Time'].astype('str').str.extract(r'(\d+[.\d]*)')
    ces__feedback__8['Chat Response Time'] = pd.to_numeric(ces__feedback__8['Chat Response Time'], errors='coerce')
 
    # Content Score
    ces__feedback__8['Content Score'] = ces__feedback__8['Content Score'].astype('str').str.extract(r'(\d+[.\d]*)')
    ces__feedback__8['Content Score'] = pd.to_numeric(ces__feedback__8['Content Score'] , errors='coerce')
    ces__feedback__8.loc[ ces__feedback__8['Content Score'].astype(float) < 1, 'Content Score' ] = (ces__feedback__8.loc[ ces__feedback__8['Content Score'].astype(float) < 1, 'Content Score' ] ) * 100
    ces__feedback__8.loc[ ces__feedback__8['Content Score'].astype(float) == 0, 'Content Score' ] = np.nan
    ces__feedback__8.loc[ ces__feedback__8['Content Score'].astype(float) < 1, 'Content Score' ]
   
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 

# # Final mapping
 

try:
    mess = 'Mapping w Master File'
    print(f"\nTry {mess}...")
   
    ces__feedback__final = ces__feedback__8.copy()
 
    ces__feedback__final['merchantid__x__channel'] = ces__feedback__final.merchant_id_after + ces__feedback__final.channel__cleaned
 
    ces__feedback__final.loc [ ces__feedback__final['merchantid__x__channel'].isna() , :].shape
 
    master_list
    before = ces__feedback__final.shape[0]
    ces__feedback__final__full = pd.merge(
                                        ces__feedback__final,
                                        master_list,
                                        how="left",
                                        on=None,
                                        left_on=['merchantid__x__channel'] ,
                                        right_on=['merchantid_x_channel'],
                                        left_index=False,right_index=False,sort=True,suffixes=("_before", "_after"),copy=True,indicator=False,validate=None,
                                    )
    after = ces__feedback__final__full.shape[0]
    if after != before:
        print(before, after)
        print("Duplicated in mapping file {}, need to remove duplicate first, sheet touch_point".format(url_mapping))
       
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
   
 

try:
       mess = 'Get column from Master File'
       print(f"\nTry {mess}...")
 
       ces__feedback__get = ces__feedback__final__full.loc[:, ['Name', 'Order Number',
              'Complaints', 'Inquiry', 'Request', 'Positive Comments', 'Ratings',
              'Customer Message', 'CES Response', 'Date Posted', 'Date Responded',
              'Resolved', 'Customer Name', 'Product', 'Start of Day Count',
              'End Of Day Count', 'Positive Seller Rating', 'Content Score',
              'Same-day Chat Response Rate', 'Chat Response Time',
              'Ship-on-Time (SOT)', 'Cancellation Rate', 'Return Rate',
              'Conversion Rate', 'Conversations', 'Product Ratings Cleared?',
              'Seller Ratings Cleared?', 'Message Center Cleared?', 'Feed Link',
              'Timestamp', 'Date', 'Ticket #', 'To', 'CC', 'Customer Name 2', 'Email',
              'Ticket Status', 'Email Resolution Date',
              'source',
              'region_after', 'merchant_id_after',
              'touchpoint__cleanned', 'store_name__final', 'channel_after',
              'business_unit', 'merchant_type',
              'distribution_model', 'group_of_company', 'category', 'merchantid__x__channel']]
except Exception as e:
       input(f"\nCannot {mess} due to {e}. Press any key to exit...")
       sys.exit()
 
 

try:
    mess = 'Rename Columns'
    print(f"\nTry {mess}...")
 
    ces__feedback__get.rename(columns = {'region_after':'Region'
                                        , 'merchant_id_after' : 'Merchant ID'
                                        , 'touchpoint__cleanned':'Touchpoint'
                                        , 'store_name__final' : 'Store Name'
                                        , 'channel_after' : 'Channel'
                                        , 'business_unit' : 'Business Unit'
                                        , 'merchant_type' : 'Merchant Type'
                                        , 'distribution_model' : 'Distribution Model'
                                        , 'group_of_company' : 'Group of Company'
                                        , 'category' : 'Category'
                                        }, inplace = True)
 
    dk = ( (ces__feedback__get['Region'].isna()) | (ces__feedback__get['Store Name'].isna())  | (ces__feedback__get['Merchant ID'].isna()) | (ces__feedback__get['Channel'].isna()))
 
    ces__feedback__get2 = ces__feedback__get.loc[~dk , :]
 
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 
 

report__data_removed = ces__feedback__get.loc[dk , ['source','Name','Region','Order Number','Store Name','Channel'] ].drop_duplicates().reset_index(drop=True)
report__data_removed
 

try:
    mess = 'Export .csv'
    print(f"\nTry {mess}...")
 
    ces__feedback__get.to_csv(r'C:\import_snowflake\ces__feedback.csv', encoding = 'utf-8-sig', index= False)
   
except Exception as e:
    input(f"\nCannot {mess} due to {e}. Press any key to exit...")
    sys.exit()
 
 
 

_try = 0
while _try < 3:
    ces__feedback__get['Date'] = pd.to_datetime(ces__feedback__get['Date'], format = '%Y-%m-%d').dt.strftime('%Y-%m-%d')
    df_import = ces__feedback__get.copy().fillna('').astype(str)
    try:
        print('\nUpload to snowflake...')
        hoangphuc__snowflake_ingestion.csv_upload__to_snowflake__v2(
                        schema = 'PHUC'
                        , tablename = 'CES__FEEDBACK'
                        , path = 'C:/import_snowflake/'
                        , df = df_import
                        , mode = hoangphuc__snowflake_ingestion.ETLMode.full_refresh
        )
        break
    except Exception as e:
        print(e)
        sec = 5
        _try += 1
        print(f'Try again after {sec} sec. Pls screenshot your screen and send to email: {contact}')
        time.sleep(sec)
 
print("Done! Press any key to exits..")
 

# # Incorrect Report
 

try_export = 0
while try_export < 3:
    try:
        mess = 'Export .xlsx report'
        print(f"\nTry {mess}...")
        with pd.ExcelWriter(os.path.join(report_folder__ces, 'ces__invalid_data.xlsx'), engine='xlsxwriter') as writer:
            region_report.to_excel(writer, sheet_name='Region_Invalid', index=False )
            touchpoint_report.to_excel(writer, sheet_name='Toupoint_Invalid', index=False )
            date_report.to_excel(writer, sheet_name='Date_Invalid', index=False )
            report_store_name_invalid.to_excel(writer, sheet_name='StoreName_Invalid', index=False )
            report__invalid_channel.to_excel(writer, sheet_name='Channel_Invalid', index=False )
            report__data_removed.to_excel(writer, sheet_name='Region_Missing', index=False )
        writer.save()
        break
    except Exception as e:
        try_export += 1
        input(f"\nCannot {mess} due to {e}. Will try again after 5 sec...")
        time.sleep(5)
 

region_report['Type of Invalid Data'] = 'Region'
region_report
 

touchpoint_report['Type of Invalid Data'] = 'Touchpoint'
touchpoint_report
 

date_report['Type of Invalid Data'] = 'Date'
date_report
 

report_store_name_invalid['Type of Invalid Data'] = 'Store Name'
report_store_name_invalid
 

report__data_removed['Type of Invalid Data'] = 'Doesnt input region'
report__data_removed
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 

 
 
 
 

