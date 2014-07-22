var bench = require('api-benchmark');

var service = {serv:"http://mrsbmapp20965/arcgis/rest/services/Public/ExternalMap/"}

bench.measure(service,{r1:"MapServer"},function(err,results){console.log(results)})