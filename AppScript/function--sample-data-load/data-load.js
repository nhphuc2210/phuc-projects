function processS3Uploads() {
    var folder = DriveApp.getFolderById("1hsIUMBjzEdzIsTFyUC5W3iGm2kSoAqke");
    var files = folder.getFiles();
    while (files.hasNext()) {
      var file = files.next();
  
      Logger.log("Input CSV:" + file.getName());
      if (file.getName().toString().indexOf("KitchenTimings") > -1) {
        processKitchenTimings(file);
      } else if (file.getName().toString().indexOf("AllItemsReport") > -1) {
        processAllItemsReport(file);
      }
    }
  }
  
  function processKitchenTimings(file) {
    var contents = Utilities.parseCsv(file.getBlob().getDataAsString());
  
    var checkNumberColumnId = 3;
    var stationColumnId = 6;
    var expediterLevelColumnId = 7;
    var firedDateColumnId = 8;
    var fulfillmentTimeColumnId = 10;
    
    var checkInfos = new Map();
    for (var i = 0; i < contents.length; ++i) {
      var row = contents[i];
      if (i == 0) {
        if (row[checkNumberColumnId] != "Check #") {
          throw ("error: Check # column not found");
        } else if (row[stationColumnId] != "Station") {
          throw ("error: Station column not found");
        } else if (row[expediterLevelColumnId] != "Expediter Level") {
          throw ("error: Expediter Level column not found");
        } else if (row[firedDateColumnId] != "Fired Date") {
          throw ("error: Fired Date column not found");
        } else if (row[fulfillmentTimeColumnId] != "Fulfillment Time") {
          throw ("error: Fulfillment Time column not found");
        }
      } else {
        const checkNumber = row[checkNumberColumnId];
  
        var timingRow = [row[firedDateColumnId],
          row[stationColumnId],
          row[expediterLevelColumnId],
          countSeconds(row[fulfillmentTimeColumnId])];
  
        if (checkInfos.has(checkNumber)) {
          var checkInfo = checkInfos.get(checkNumber);
          saveTimingIntoCheckInfo(checkInfo, timingRow);
        } else {
          var checkInfo = [checkNumber, '', '', '', '', ''];
          saveTimingIntoCheckInfo(checkInfo, timingRow);
          checkInfos.set(checkNumber, checkInfo);
        }
      }
    }
    file.setTrashed(true);
  
    var spreadsheet = SpreadsheetApp.openById("1imqc5tNEShcr7YNTHSmJT8oiwkSDtqpHh7x4AUZaxXU");
    var sheet = spreadsheet.getSheets()[0];
    for (let [key, value] of checkInfos ) {
      var checkInfo = value;
      // compute expo1 - dough for oven duration
      if (checkInfo[3].length != 0 && checkInfo[2].length != 0) {
        const ovenDuration = (Number(checkInfo[3]) - Number(checkInfo[2])).toFixed(2);
        checkInfo.push(ovenDuration > 0 ? ovenDuration : "");
      }
      // compute expo 1 = expo 2 for total end to end duration
      if (checkInfo[3].length != 0 && checkInfo[4].length != 0) {
        const totalDuration = (Number(checkInfo[3]) + Number(checkInfo[4])).toFixed(2);
        checkInfo.push(totalDuration > 0 ? totalDuration : "");
      }
      Logger.log(checkInfo);
      sheet.appendRow(checkInfo);
    }
  }
  function processAllItemsReport(file) {
    var contents = Utilities.parseCsv(file.getBlob().getDataAsString());
    var fileName = file.getName();
    var reportDate = new Date(+fileName.substring(0, 4),
      +fileName.substring(4, 6) - 1,
      +fileName.substring(6, 8));
  
    const adjaruliBoat = 'Adjaruli Boat';
    const chickenBoat = 'Chicken Boat';
    const lobianiBoat = 'Lobiani Boat';
    const stroganoffBoat = 'Stroganoff Boat';
    const veggieBoat = 'Veggie Boat';
  
    const menuItemColumnId = 6;
    const itemQtyColumnId = 12;
    var boatsSold = new Map();
  
    for (var i = 0; i < contents.length; ++i) {
      var row = contents[i];
      if (i == 0) {
        if (row[menuItemColumnId] != "Menu Item") {
          throw ("error: Menu Item not found");
        } else if (row[itemQtyColumnId] != "Item Qty") {
          throw ("error: Item Qty not found");
        }
      } else {
        if (row[menuItemColumnId] == adjaruliBoat) {
          boatsSold.set(adjaruliBoat, +row[itemQtyColumnId]);
        } else if (row[menuItemColumnId] == chickenBoat) {
          boatsSold.set(chickenBoat, +row[itemQtyColumnId]);
        } else if (row[menuItemColumnId] == lobianiBoat) {
          boatsSold.set(lobianiBoat, +row[itemQtyColumnId]);
        } else if (row[menuItemColumnId] == stroganoffBoat) {
          boatsSold.set(stroganoffBoat, +row[itemQtyColumnId]);
        } else if (row[menuItemColumnId] == veggieBoat) {
          boatsSold.set(veggieBoat, +row[itemQtyColumnId]);
        }
      }
    }
    file.setTrashed(true);
  
    var totalBoatsSold = 0;
    boatsSold.forEach(b => totalBoatsSold += b);
  
    var spreadsheet = SpreadsheetApp.openById("1NOgYg7aVYsVyVOOIGB8Kg6brlQ3j-XL0_S7zr0TKryc");
    var sheet = spreadsheet.getSheets()[0];
  
    var processedRow = [reportDate,
      boatsSold.get(adjaruliBoat),
      boatsSold.get(chickenBoat),
      boatsSold.get(lobianiBoat),
      boatsSold.get(stroganoffBoat),
      boatsSold.get(veggieBoat),
      totalBoatsSold
    ];
    Logger.log(processedRow);
    sheet.appendRow(processedRow);
  }
  
  function countSeconds(fulfillmentTime) {
    if (fulfillmentTime.length == 0) {
      return 0;
    }
    fulfillmentTime = fulfillmentTime.replace('and ', '').replace(',', '');
  
    var terms = fulfillmentTime.split(" ");
    if (terms.length % 2 != 0) {
      throw ("error: Unexpected input: " + fulfillmentTime);
    }
  
    var seconds = 0;
    for (var i = 0; i < terms.length; i = i + 2) {
      if (terms[i + 1] == "minute" || terms[i + 1] == "minutes") {
        seconds += parseInt(terms[i]) * 60;
      } else if (terms[i + 1] == "second" || terms[i + 1] == "seconds") {
        seconds += parseInt(terms[i]);
      } else if (terms[i + 1] == "millisecond" || terms[i + 1] == "milliseconds") {
      } else if (terms[i + 1] == "hour" || terms[i + 1] == "hours") {
        seconds += parseInt(terms[i]) * 60 * 60;
      } else {
        throw ("error: Unexpected input: " + fulfillmentTime);
      }
    }
  
    return Number(seconds / 60).toFixed(2);
  }
  
  function saveTimingIntoCheckInfo(checkInfo, timingRow) {
    const firedDate = timingRow[0];
    const station = timingRow[1];
    const expoLevel = timingRow[2];
    const duration = timingRow[3];
  
    if (checkInfo[1].length == 0) {
      checkInfo[1] = firedDate;
    }
    if (station == 'Drinks') {
      checkInfo[5] = duration;
    } else if (station == 'Dough'){
      checkInfo[2] = duration;
    } else if (expoLevel == '1') {
      checkInfo[3] = duration;
    } else if (expoLevel == '2') {
      checkInfo[4] = duration;
    }
  }