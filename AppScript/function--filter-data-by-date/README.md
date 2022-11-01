
## BY TEXT V2

```js

function myFunction() {
var sss = SpreadsheetApp.openById('1qHRqfQx5CkJ7WqXfCyIHRrA-7M-gwNAAuGB8BDuhOGI'); //replace with source ID
var ss = sss.getSheetByName('DailyCount'); //replace with source Sheet tab name
var range = ss.getRange('A:L');      //assign the range you want to copy
var rawData = range.getValues()     // get value from spreadsheet 1
var data = []                       // Filtered Data will be stored in this array
for (var i = 0; i< rawData.length ; i++){
  const date_filter = new Date('2022-10-05 13:00:00 -0500');
  const selected_date = new Date( rawData[i][0] )

  const convert_date_filter = Utilities.formatDate(date_filter, 'Eastern Daylight Time', 'yyyy-MM-dd')
  const convert_selected_date = Utilities.formatDate(selected_date, 'Eastern Daylight Time', 'yyyy-MM-dd')

  Logger.log( selected_date )

  // Logger.log( Utilities.formatDate( rawData[i][0].toString() , 'Eastern Daylight Time', 'yyyy-MM-dd') );

if( convert_selected_date === convert_date_filter )            // Check to see if column K says ipad if not skip it
{
data.push(rawData[i])
Logger.log( 'GET' );
}
}

var tss = SpreadsheetApp.openById('1qHRqfQx5CkJ7WqXfCyIHRrA-7M-gwNAAuGB8BDuhOGI'); //replace with destination ID
var ts = tss.getSheetByName('copied'); //replace with destination Sheet tab name
Logger.log(data)
ts.getRange(ts.getLastRow()+1, 1, data.length, data[0].length).setValues(data);

}
```