
# **Google Data Studio**

    - Sales per month (line chart or bar chart)
    - Leads per campaigns (ranking chart)
    - Sales per lead campaigns (ranking chart)

url = https://datastudio.google.com/u/1/reporting/fa7aa19f-e191-41be-b97e-acb2cb31dd76/page/OiX5C/edit

bigquery = https://console.cloud.google.com/bigquery?authuser=1&project=danh-298607&ws=!1m0

website for branding = https://www.quasarex.com
    

## **Raw Data**
1. raw-data/CustomBookingFact.xlsx
2. raw-data/CustomInquiryFact.xlsx

**Step:**
1. Clean up CustomInquiryFact > Column LeadSource > replace utm tagging url to ***CampaignSource, CampaignMedium, CampaignName, CampaignTerm, CampaignContent***

    script > https://stackoverflow.com/questions/5074803/retrieving-parameters-from-a-url

    or

    ```python
    def transformation_inquiry(file):
    """Transformar los datos de consulta

    Args:
        file (dataframe)

    Returns:
        dataframe
    """
    file.fillna('', inplace=True)
    data = []
    file['LeadSource2'] = file['LeadSource'].copy()
    file['urlSplit'] = file['LeadSource2'].tolist()
    for x in range(len(file['urlSplit'].tolist())):
        data.append(parse_qs(urlparse(file['LeadSource'].tolist()[x]).query))
    for x in range(len(data)):
        try:
            file.at[x,'CampaignSource']=data[x]['utm_source'][0]
        except:
            pass
        try:
            file.at[x,'CampaignName']=data[x]['utm_campaign'][0]
        except:
            pass
        try:
            file.at[x,'CampaignTerm']=data[x]['utm_term'][0]
        except:
            pass
        try:
            file.at[x,'CampaignContent']=data[x]['utm_content'][0]
        except:
            pass
        try:
            file.at[x,'CampaignMedium']=data[x]['utm_medium'][0]
        except:
            pass
        file.at[x,'DateOfFirstContact'] = datetime.datetime.strptime(file.iloc[x]['DateOfFirstContact'].split()[0], "%m/%d/%Y").strftime('%d-%m-%Y')
    del file['urlSplit']
    del file['LeadSource2']
    file = file.reset_index(drop=True)  
    return file
    ```

2. Clean up date format
    
    Column = **DateBooked** in Booking file and **DateOfFirstContact** in Inquiry file

    ```python
    datetime.datetime.strptime(file.iloc[i]['DateBooked'], "%m/%d/%Y %I:%M:%S %p").strftime('%d-%m-%Y')
    ```


3. Ingest to BigQuery (testing environment)

4. Import to Google Data Studio.

- Sales per month (line chart or bar chart)
- Leads per campaigns (ranking chart)
- Sales per lead campaigns (ranking chart)


## **Definitions**
**Leads per campaign =** 
```sql
select 
LeadSource, CampaignSource, CampaignMedium, CampaignName, CampaignTerm, CampaignContent
, count(distinct concat(email, DateOfFirstContact)) as leads
from inquiry
group by 1,2,3,4,5,6
```

**Sales data =**
```sql
with sales_data as (
    select email, DateBooked, sum(TotalRevenues) as sales
    from Booking
    group by 1,2
)
```

**sales per leads campaign=**

leads campaign = concat(email, LeadSource)

Booking links Inquiry by Email

Email is exists in booking but not exist in inquiry => lead campaigns = 'Others'


    CampaignSource = utm_source
    CampaignMedium = utm_medium
    CampaignName = utm_campaign
    CampaignTerm = utm_term

```python
def transformation_inquiry(file):
"""Transformar los datos de consulta

Args:
    file (dataframe)

Returns:
    dataframe
"""
file.fillna('', inplace=True)
data = []
file['LeadSource2'] = file['LeadSource'].copy()
file['urlSplit'] = file['LeadSource2'].tolist()
for x in range(len(file['urlSplit'].tolist())):
    data.append(parse_qs(urlparse(file['LeadSource'].tolist()[x]).query))
for x in range(len(data)):
    try:
        file.at[x,'CampaignSource']=data[x]['utm_source'][0]
    except:
        pass
    try:
        file.at[x,'CampaignName']=data[x]['utm_campaign'][0]
    except:
        pass
    try:
        file.at[x,'CampaignTerm']=data[x]['utm_term'][0]
    except:
        pass
    try:
        file.at[x,'CampaignContent']=data[x]['utm_content'][0]
    except:
        pass
    try:
        file.at[x,'CampaignMedium']=data[x]['utm_medium'][0]
    except:
        pass
    file.at[x,'DateOfFirstContact'] = datetime.datetime.strptime(file.iloc[x]['DateOfFirstContact'].split()[0], "%m/%d/%Y").strftime('%d-%m-%Y')
del file['urlSplit']
del file['LeadSource2']
file = file.reset_index(drop=True)  
return file

```