
# **POSTGRE - EXTRACT DATA FROM JSONB**

<br />

# **E.g 1:**

### **Job Descriptions:**

I have a jsonb field with an array like this one below:

```json
[  
   {  
      "type":"discount",
      "title":"Discount 10%"
   },
   {        
      "file":"zx5rP8EoacyfhqGndcSOnP8VYtkr9Ya8Nvf7oYL98YDsM1CLMYIurYvfVUU4AGkzBsovwssT0bq.pdf",
      "type":"menu",
      "title":"Some menu title etc"
   }
]
```
    
I want to get the **file** attribute in case there is a **type=menu** in the array.

What I managed to do is to know if there is one, but how can I eventually extract the file value?

```sql
case when offers @> '[{"type":"menu"}]' then true else false end
```

I don't want to do something like this below because the array may not contain a discount type.

```sql
offers->1->'file'
```
    
#

## **SOLUTIONS**
<br />

Use jsob_array_elements() and ->> operator

```sql
with a_table(json_col) as (
values (
'[  
   {  
      "type":"discount",
      "title":"Discount 10%"
   },
   {        
      "file":"zx5rP8EoacyfhqGndcSOnP8VYtkr9Ya8Nvf7oYL98YDsM1CLMYIurYvfVUU4AGkzBsovwssT0bq.pdf",
      "type":"menu",
      "title":"Some menu title etc"
   }
]'::jsonb)
)

select value->>'file' as filename
from a_table,
lateral jsonb_array_elements(json_col)
where value->>'type' = 'menu'
FROM "schema".tbl_name
```

| filename  | 
| :------------:|
| zx5rP8EoacyfhqGndcSOnP8VYtkr9Ya8Nvf7oYL98YDsM1CLMYIurYvfVUU4AGkzBsovwssT0bq.pdf | 

<br />

<br />

<br />

<br />

# **E.g 2:**

### **Job Descriptions:**

In my database table I have a column named data and that column's type is jsonb. Here is a sample json of the column.


```json
{"query": {"end-date": "2016-01-31", "start-date": "2016-01-01", "max-results": 1000, "start-index": 1 }}
```
    
I need to get the data from the 'start date' inside the 'query' element. How get the data from the start date from a pgsql query

    
#

## **SOLUTIONS**
<br />

```sql
select json_extract_path(data::json,'query','start-date') as test 
FROM "schema".tbl_name
```

# **E.g 3:**

### **Job Descriptions:**

I have a table in my database, which contains character varying column and this column has json. I need to write a query, which will somehow parse this json into separate columns.

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/sql-postgre--extract-data-from-jsonb/.data/x7b90.png)


#

## **SOLUTIONS**
<br />

```sql
SELECT 
   id, 
   data::json->'name' as name,
   data::json->'author' ->> 'last_name' as author
FROM books;
```