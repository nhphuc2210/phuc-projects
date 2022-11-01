
# **REMOVE DUPLICATES**

```js
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
```