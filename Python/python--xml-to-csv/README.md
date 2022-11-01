
# **Mapping 2 XML Messages**

## **JOB REQUIREMENTS**
<br />

##### **Job Post URL:** `<link>` : ***<https://www.upwork.com/jobs/~01fefecfe45d497c21>***
<br />

### **Job Descriptions:**

    I have two XML messages from IATA that I need mapped together.

    They are very similar and need to be mapped between each other with the output in an CSV or XLS file.

    Approximately 3,000 rows need to be mapped 
    but the bulk of the effort can be automated by someone 
    with the proper knowledge. 
    
    The field names are for the most part an exact match 
    (except for the route of course).

    I will provide the CSV file that contains 
    the output of the original message 
    and the two XSD schema files.



## **SOLUTIONS**
<br />

**XML FILES**

<br />

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/python--xml-to-csv/.data/xml-sample-file.jpg)

<br />

**CONVERTED TO DATAFRAME**

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/python--xml-to-csv/.data/result-csv.jpg)

<br />

```python
for employee in xml.findall("employee"):

    if(employee):
       
       # EXTRACT EMPLOYEE DETAILS  
      name = employee.find("name")
      role = employee.find("role")
      age = employee.find("age")
      csv_line = [name.text, role.text, age.text]

      # ADD A NEW ROW TO CSV FILE
      csvfile_writer.writerow(csv_line)
```
<br />
