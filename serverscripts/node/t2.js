var request = require('request');
console.log("loaded")
var rCount = 0;
//var service = "http://mrsbmapp20965/arcgis/rest/services/Public/ExternalMap/MapServer/0/query?f=json&where=1%3D1&spatialRel=esriSpatialRelIntersects&&returnGeometry=false&maxAllowableOffset=10&outFields=OBJECTID&outSR=102100";
var service = "http://www.google.com";
var initialTime = Date.now();
var timeArr=[];
for (var i=0;i<100;i++){
request(service,function(data){
  console.log("YO")
  var currTime = Date.now();
  timeArr[rCount]=currTime-initialTime;
  rCount++;
  if(rCount === 99) console.log(currTime-initialTime,timeArr)
})
}