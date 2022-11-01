
# **Excel. Extract data from same range in all sheets in one workbook, including formatting**

## **JOB REQUIREMENTS**
<br />

<!-- ##### **Job Post URL:** `<link>` : ***<https://www.upwork.com/nx/wm/pre-hire/f/offer/21667045>*** -->
<br />

### **Job Descriptions:**

    I have many workbooks with up to 200 sheets.  

    For each workbook, I would like to be able to extract the same range (a single column with 72 rows) from all the sheets to a new workbook, with each range pasted into the next available column.

    The most important part is getting the formatting to come across.

    I have created a dummy workbook with 4 tabs with a basic version of my workbooks.  The final tab is what I would like the data to look like.

    Please feel free to call me if you have any questions


<br />

#
## **SOLUTIONS**

<br />

**Before - Files need to combine:**

![](.data/before-file-need-to-combine.jpg)

<br />

**After - Combined**

![](.data/after-combined-by-button.jpg)



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

