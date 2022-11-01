function processS3Uploads() {
    var folder = DriveApp.getFolderById("1hsIUMBjzEdzIsTFyUC5W3iGm2kSoAqke");
    var files = folder.getFiles();
    clearOldData_AllSheet('1qQC53hOXauKjkcumqecc5zIdsbq4u8QO0xZbQ__CdJw');
    
    while (files.hasNext()) {
      var file = files.next();
      Logger.log('==== file = ' + file.getName());
      
      if (file.getName().toString().indexOf("PaymentDetails_") > -1) {
        processCsv_6col(file)
        true
      } else if (file.getName().toString().indexOf("-PaymentDetails") > -1) {
        processCsv_33col(file)
        true
      }
    }
    
  }
  
  
  function processCsv_6col(file) {
      var spreadsheet = SpreadsheetApp.openById("1qQC53hOXauKjkcumqecc5zIdsbq4u8QO0xZbQ__CdJw");
      var sheet = spreadsheet.getSheetByName('raw_processPaymentDetails');
      
      // Parses CSV file into data array.
      let contents = Utilities.parseCsv(file.getBlob().getDataAsString());
      
      if ( sheet.getLastRow() != 0 ) {
        Logger.log('==== Get data without header');
        contents.splice(0, 1);
      } else {
        Logger.log('==== Get data with header');
      }
      
      colDate = 0;
      colPhone = 4;
      colTotal = 2;
      otherType = 33;
      var push_data = [];
  
      for (var i = 0; i < contents.length; ++i) {
        var row  =contents[i];
        if (i == 0  && startRow > 1) {
            push_data.push([row[colDate],row[colPhone],row[colTotal],'otherType']);
        } else if ( row[colPhone] != "") {
            push_data.push([row[colDate],row[colPhone],row[colTotal],'']);
        }
      }  
  
      // Gets the row and column coordinates for next available range in the spreadsheet. 
      let startRow = sheet.getLastRow() + 1;
      let startCol = 1;
      
      // Determines the incoming data size.
      let numRows = push_data.length;
      let numColumns = push_data[0].length;
  
      // Appends data into the sheet.
      sheet.getRange(startRow, startCol, numRows, numColumns).setValues(push_data);
      return true; // Success.
  }
  
  function processCsv_33col(file) {
      var spreadsheet = SpreadsheetApp.openById("1qQC53hOXauKjkcumqecc5zIdsbq4u8QO0xZbQ__CdJw");
      var sheet = spreadsheet.getSheetByName('raw_processPaymentDetails');
      // Gets the row and column coordinates for next available range in the spreadsheet. 
      let startRow = sheet.getLastRow() + 1;
      let startCol = 1;
      
      // Parses CSV file into data array.
      let contents = Utilities.parseCsv(file.getBlob().getDataAsString());
      
      if ( sheet.getLastRow() != 0 ) {
        Logger.log('==== Get data without header');
        contents.splice(0, 1);
      } else {
        Logger.log('==== Get data with header');
      }
      
      colDate = 5;
      colPhone = 35;
      colTotal = 18;
      otherType = 33;
      var push_data = [];
  
      for (var i = 0; i < contents.length; ++i) {
        var row  =contents[i];
        if (i == 0 && startRow == 1) {
            push_data.push([row[colDate],row[colPhone],row[colTotal],'otherType']);
        } else if ( row[colPhone] != ""  && row[otherType] == "") {
            push_data.push([row[colDate],row[colPhone],row[colTotal],row[otherType]]);
        }
      }  
  
      
      // Determines the incoming data size.
      let numRows = push_data.length;
      let numColumns = push_data[0].length;
  
      // Appends data into the sheet.
      sheet.getRange(startRow, startCol, numRows, numColumns).setValues(push_data);
      return true; // Success.
  }
  
  function clearOldData_AllSheet(file_id) {
    var sheet_names = ['raw_processPaymentDetails']
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
  
  
  
  
  
  
  
  