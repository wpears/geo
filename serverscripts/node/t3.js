var request = require('request');
console.log("Loaded");
var rCount = 0;
var service = "http://mrsbmapp20965/arcgis/rest/services/Public/ExternalMap/MapServer/0/query?f=json&where=1%3D1&spatialRel=esriSpatialRelIntersects&&returnGeometry=false&maxAllowableOffset=10&outFields=OBJECTID&outSR=102100";
var initialTime = Date.now();
var timeArr=[];
var total=0;
var max =100;
var par = 20;

function makeReqs(){
  var lastTime=Date.now();
  var smallCount=0;
  for(var i=0;i<par&&total<max;i++){
    total++;
    request(service,function(err,data){
      if (err) throw err;
      var currTime = Date.now();
      timeArr[rCount]=currTime-lastTime;
      rCount++;
      smallCount++;
      if(smallCount === par-1)makeReqs();
      if(rCount===max-1) console.log(timeArr,currTime-initialTime)
    })
  }
}
makeReqs();