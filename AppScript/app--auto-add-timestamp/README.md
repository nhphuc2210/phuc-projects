
# **Auto-update With A New Date Every Time Anything In Column E**


## **Job Descriptions**


<br />

    See Column C in the attached spreadsheet. 

    I created this formula "=IF(E5 ="", "", TODAY())". 

    The goal was so that if anything is added to column E in the same row, the date would automatically be added. 

    However, the date was supposed to be static. So if an item was added on 9/19, that date would populate and stay that way. 

    However, the issue is that the date is dynamic and will auto-update with a new date every time anything in column E is updated. 

    I need someone to adjust the formula to make it work the way I'd like.


<br />


## **Solutions**

Short Video shows how it works > https://www.loom.com/share/ca70fcde8399463188f5c1f4dee0df6f

Have no function in Google Sheet. But we can use AppScript to build a custom function that will be triggered when any cells a column is updated.

```js
function setUpTrigger(e) {
  ScriptApp.newTrigger('add_time')
  .forSpreadsheet("1-NWL6nHMP8Y9_RZmz9Mi5TNYREZYVhprqwsugofo-u0")
  .onEdit()
  .create();
}

function add_time(e) {
    // my function
}
```