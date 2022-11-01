
# **AUTO GENERATE SUB MENU**

```js
function installFunctions() {
  var ss = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var get_range_original = ss.getRange(2, 1, ss.getLastRow()-1, 1).getValues();
  var range_unique = removeDups(get_range_original);
  var date_strings = array_date_to_string(range_unique);
  var ui = SpreadsheetApp.getUi();
  var menu = ui.createMenu('Custom Menu')
  .addItem('First item', 'menuItem1')
  .addSeparator();
  var subMenu = ui.createMenu('Sub-menu');
  for (var i = 0; i < range_unique.length; i++) {
    var dynamicMenu = date_strings[i];
    this[dynamicMenu] = dynamicItem(i); // Added
    subMenu.addItem(dynamicMenu,dynamicMenu); // Modified
  }
  menu.addSubMenu(subMenu).addToUi();
}

function dynamicItem(i) { // Added
  return function() {
    var sheet = SpreadsheetApp.getActiveSheet();
    sheet.getRange(2, i + 1, sheet.getLastRow() - 1, 1).activate();
  }
}

function array_date_to_string(array) {
  var outArray = [];
  for (var n = 0; n < array.length; n++) {
    get_string = Utilities.formatDate(new Date(array[n].toString()), "GMT+7", "yyyy-MM-dd");
    outArray.push(get_string);
  };
  outArray.sort();
  return outArray;
}




function removeDups(array) {
  var outArray = [];
  array.sort();
  outArray.push(array[0]);
  for(var n in array){
    // Logger.log(outArray[outArray.length-1]+'  =  '+array[n]+' ?');
    if(outArray[outArray.length-1].toString() != array[n].toString() ){
      outArray.push(array[n]);
    }
  }
  // Logger.log( outArray );
  return outArray;
}

installFunctions(); // Added

function onOpen() {} // Modified: This can be used as the simple trigger.

function onEdit() {} // Modified: This can be used as the simple trigger.

function onChange() {} // Added: Please install OnChange event trigger to this function.

```