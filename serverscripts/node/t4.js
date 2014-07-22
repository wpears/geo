var req = require('request');
var time=Date.now();
var server = "http://mrsbmapp20965/arcgis/rest/services/Public/ExternalMap/MapServer/0/query?f=json&where=1%3D1&spatialRel=esriSpatialRelIntersects&&returnGeometry=false&maxAllowableOffset=10&outFields=OBJECTID&outSR=102100"
req(server,function(e,d){console.log(Date.now()-time)})