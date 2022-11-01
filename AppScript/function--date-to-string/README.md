
# **CONVERT ARRAY DATE TO STRING**

```js
function array_date_to_string(array) {
  var outArray = [];
  for (var n = 0; n < array.length; n++) {
    get_string = Utilities.formatDate(new Date(array[n].toString()), "GMT+7", "yyyy-MM-dd");
    outArray.push(get_string);
  };
  outArray.sort();
  return outArray;
}
```