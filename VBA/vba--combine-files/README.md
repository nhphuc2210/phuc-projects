
# **Excel VBA copy paste multiple files onto one tab**

## **JOB REQUIREMENTS**
<br />

<!-- ##### **Job Post URL:** `<link>` : ***<https://www.upwork.com/nx/wm/pre-hire/f/offer/21667045>*** -->
<br />

### **Job Descriptions:**

    Please create Excel VBA macro. For instance I have 4 xls files named master.xls one.xls two.xls three.xls located in one folder.

    All files are placed in c drive folder macro. C:\macro\

    Create a macro in master.xls that runs as follows. Copies cells A1:P200 pastes to master --from all 3 files one at a time.

    Do not use a for loop because more than the above files can be found in the folder. Meaning the files one two three can be more than them.

    Let me know the script and I will copy and paste --via insert into module --of Excel. Thanks.


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

### **Client's Requirements:**

> Combine every file to one sheet via copy/paste

> Not create different tabs. 

> In the end there must be only one tab that has all the different worksheet files

> VBA only - I can't share a python app to my coworkers

<br />

#
## **SOLUTIONS**

<br />

**Before - Files need to combine:**

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/vba--combine-files/.data/before-file-need-to-combine.jpg)

<br />

**After - Combined**

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/vba--combine-files/.data/after-combined-by-button.jpg)

**Short Video**


https://www.loom.com/embed/3bf5721dea064a69b590472bc48a6294



### **Source code - VBA**

<br />


```python
Sub Get_Data()

Application.ScreenUpdating = False
Application.EnableEvents = False
Application.Calculation = xlCalculationManual

Sheet_Name = "2005"
Set New_Workbook = ThisWorkbook

Set File_Dialog = Application.FileDialog(msoFileDialogFolderPicker)
File_Dialog.AllowMultiSelect = False
File_Dialog.Title = "Select the Excel Files"
If File_Dialog.Show <> -1 Then
    Exit Sub
End If

File_Path = File_Dialog.SelectedItems(1) & "\"
File_Name = Dir(File_Path & "*.xls*")

'ActiveColumn = 0
active_row = 3
Do While File_Name <> ""
...
Loop

End Sub
```

<!-- 


    Set File = Workbooks.Open(Filename:=File_Path & File_Name)
    Set TotalRange = File.Worksheets(Sheet_Name).UsedRange
    Set TotalRange = TotalRange.Offset(1, 0).Resize(TotalRange.Rows.Count - 1, _
                                               TotalRange.Columns.Count)
    TotalRange.Copy
    
    'ActiveColumn = ActiveColumn + 1
      
    active_row = active_row - 1
    New_Workbook.Worksheets("Sheet1").Cells(active_row, 1).PasteSpecial Paste:=xlPasteAll
    
    row_number = File.Worksheets(1).UsedRange.Rows.Count
    active_row = active_row + row_number
    
    'ActiveColumn = ActiveColumn + File.Worksheets(1).UsedRange.Columns.Count
    
    'MsgBox File_Name
    File.Application.CutCopyMode = False
    File.Close True
    
    File_Name = Dir() -->

