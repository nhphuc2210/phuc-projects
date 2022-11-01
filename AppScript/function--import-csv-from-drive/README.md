```js
function processS3Uploads() {
  var folder = DriveApp.getFolderById("1hsIUMBjzEdzIsTFyUC5W3iGm2kSoAqke");
  var files = folder.getFiles();
  clearOldData_AllSheet('1qQC53hOXauKjkcumqecc5zIdsbq4u8QO0xZbQ__CdJw');
  
  while (files.hasNext()) {
    var file = files.next();
    Logger.log('==== file = ' + file.getName());
    
    if (file.getName().toString().indexOf("PaymentDetails_") > -1) {
      processCsv_(file, 'processPaymentDetails_')

    } else if (file.getName().toString().indexOf("-PaymentDetails") > -1) {
      processCsv_(file, 'processPaymentDetails__')
    }
  }
}


function processCsv_(file, target_sheet) {
  try {
    const CSV_HEADER_EXIST = true;
    var spreadsheet = SpreadsheetApp.openById("1qQC53hOXauKjkcumqecc5zIdsbq4u8QO0xZbQ__CdJw");
    var sheet = spreadsheet.getSheetByName(target_sheet);
    
    // Parses CSV file into data array.
    let data = Utilities.parseCsv(file.getBlob().getDataAsString());
    
    if ( sheet.getLastRow() != 0 ) {
      Logger.log('==== Get data without header');
      data.splice(0, 1);
    } else {
      Logger.log('==== Get data with header');
    }
    
    
    // Gets the row and column coordinates for next available range in the spreadsheet. 
    let startRow = sheet.getLastRow() + 1;
    let startCol = 1;
    
    // Determines the incoming data size.
    let numRows = data.length;
    let numColumns = data[0].length;

    // Appends data into the sheet.
    sheet.getRange(startRow, startCol, numRows, numColumns).setValues(data);
    return true; // Success.

  } catch {
    return false; // Failure. Checks for CSV data file error.
  }
}


function clearOldData_AllSheet(file_id) {
  var sheet_names = ['processPaymentDetails_','processPaymentDetails__']
  for (var i = 0; i < sheet_names.length; ++i ) {
      sheet_name = sheet_names[i];
      clearOldData_InSheet(file_id, sheet_name);
  } 
  Logger.log('clearOldData_AllSheet function successfully!');
}


function clearOldData_InSheet(file_id, sheet_name) {
  try {
      var sheet = SpreadsheetApp
                    .openById(file_id)
                    .getSheetByName(sheet_name);
            lastRow = sheet.getLastRow();
            lastCol = sheet.getMaxColumns();
            range = sheet.getRange(1,1,lastRow,lastCol);
            Logger.log('==== Old Data Deleted, Sheet = ' + sheet_name);
      range.clear();
  } catch {
    Logger.log(`${sheet_name} has nothing to delete!`);
  }
}


```