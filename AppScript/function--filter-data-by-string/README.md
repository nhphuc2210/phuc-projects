# **FILTER DATA**

## BY TEXT V1
```js

function myFunction() {
var sss = SpreadsheetApp.openById('1qHRqfQx5CkJ7WqXfCyIHRrA-7M-gwNAAuGB8BDuhOGI'); //replace with source ID
var ss = sss.getSheetByName('DailyCount'); //replace with source Sheet tab name
var range = ss.getRange('A:L');      //assign the range you want to copy
var rawData = range.getValues()     // get value from spreadsheet 1
var data = []                       // Filtered Data will be stored in this array
for (var i = 0; i< rawData.length ; i++){
if(rawData[i][1] == "abc")            // Check to see if column K says ipad if not skip it
{
data.push(rawData[i])
}
}

var tss = SpreadsheetApp.openById('1qHRqfQx5CkJ7WqXfCyIHRrA-7M-gwNAAuGB8BDuhOGI'); //replace with destination ID
var ts = tss.getSheetByName('copied'); //replace with destination Sheet tab name
// Logger.log(data)
ts.getRange(ts.getLastRow()+1, 1, data.length, data[0].length).setValues(data);

}

```


## BY TEXT V2

```js
function myFunction() {
  var sss = SpreadsheetApp.openById('1kL96dRm3Z8XBtMXnSzUARxR1b34-njlkZQ1sU0c3g1s'); //replace with source ID
  var ss = sss.getSheetByName('4cat'); //replace with source Sheet tab name
  var range = ss.getRange('A:I'); //assign the range you want to copy
  var data = range.getValues();

  var tss = SpreadsheetApp.openById('1u7547KaniKHLUJn2v-ezN4l8ZcxE4viCFcoxsA904MI'); //replace with destination ID
  var ts = tss.getSheetByName('Sheet1'); //replace with destination Sheet tab name
  ts.getRange(ts.getLastRow()+1, 1, data.length, data[0].length).setValues(data);

  var range = ts.getRange(ts.getLastRow()+1, 1, data.length, data[0].length)
  var rawData = range.getValues()     // get value from spreadsheet 2
  var data = filterByText(rawData, 10, iPad); // rawData is now sorted.
  range.clear();

  var powerRange = ts.getRange(ts.getLastRow()+1, 1, data.length, data[0].length);

  powerRange.setValues(data);
} 

function filterByText(data, columnIndex, values) {
    var value = values;
    if (data.length > 0) {
        if (typeof columnIndex != "number" || columnIndex > data[0].length) {
            throw "Please, can you choose a valid column index?";
        }
        var r = [];
        if (typeof value == "string") {
            var reg = new RegExp(escape(value).toUpperCase());
            for (var i = 0; i < data.length; i++) {
                if (columnIndex < 0 && escape(data[i].toString()).toUpperCase().search(reg) != -1 || columnIndex >= 0 && escape(data[i][columnIndex].toString()).toUpperCase().search(reg) != -1) {
                    r.push(data[i]);
                }
            }
            return r;
        } else {
            for (var i = 0; i < data.length; i++) {
                for (var j = 0; j < value.length; j++) {
                    var reg = new RegExp(escape(value[j]).toUpperCase());
                    if (columnIndex < 0 && escape(data[i].toString()).toUpperCase().search(reg) != -1 || columnIndex >= 0 && escape(data[i][columnIndex].toString()).toUpperCase().search(reg) != -1) {
                        r.push(data[i]);
                        j = value.length;
                    }
                }
            }
            return r;
        }
    } else {
        return data;
    }
}

```