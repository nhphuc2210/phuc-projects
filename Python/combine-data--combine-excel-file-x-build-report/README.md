
# **COMBINE DATA and ANALYSIS**

## **JOB REQUIREMENTS**
<br />

>##### **Job Post URL:** `<link>` : ***<https://www.upwork.com/jobs/~018293e8f91d477607>***
<br />

### **Job Descriptions:**

    I have excel data that shows inventory reconciliation differences. 
    
    The data in the different spreadsheet is in identical format. Each spreadsheet is for a different month end.  
    
    I need a spreadsheet built that will do the following.  
        - Map to the different spreadsheets and comine data into one table.  Not all inventory items exist in every spreadsheet.  
        - I only care about the most recent months items and what the differences have been in the previous month and month before etc.
        - The end result would list the items in the most recent spreadsheet and then a colum for recent month quanity, then previous month quantity, etc.  
    
    I can do it via pivot tables and lookups but I want a better and faster way.
    
    I also want to highlight rows where the quantity difference is the same in each month.
    
    I have attached 3 spreadsheets as example and also what I want the Inventory Reconcilation Analyzer Spreadheet to look like.

<br />
Other requirements:

    I have hundreds of excel files in a folder 
    that are all formatted the same.  

    I need specific data from each excel workbook 
    compiled into a new separate workbook.

    I think one easy way to do 
    this is to write a macro or script 
    that will open each workbook, 
    grab the needed data, paste it to the new workbook, 
    open the next excel workbook, 
    grab the data, paste it to 
    the new workbook a few rows down and repeat.  

    Open to suggestions on how best to complete project.

<br />

<br />

<br />

#
## **SOLUTIONS**
<br />

### **Before**
**All excel files needs to combine (put into 1 folder)**

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/combine-data--combine-excel-file-x-build-report/.data/file-need-to-combine.jpg)

<br />

### **After**
![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/combine-data--combine-excel-file-x-build-report/.data/outcome-report.jpg)


Here is short video of application that you will run by yourself
> **Short Video in Loom** `<link>` : https://www.loom.com/share/acf16b40a0c14df0aab2fd94ff147bf2

Here is testing result
> **Testing file:** `<link>` : ***<https://github.com/nhphuc2210/previous-similar-projects/blob/main/combine-data--combine-excel-file-x-build-report/testing_result.csv>***

<br />

**What tools do you use for data mining and visualization?**
```python
# python
import dateparser
import os,sys
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
```
