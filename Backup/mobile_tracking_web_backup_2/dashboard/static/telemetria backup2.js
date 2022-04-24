var fs = require('fs');
var initSqlJs = require('sql-wasm.js');
var filebuffer = fs.readFileSync('C:\Users\zfern\Documents\Programming Projects\Python\Projects\Homologação\Servidor - TCC\mobile_tracking_web\telemetria.db');

initSqlJs().then(function(SQL){
  // Load the db
  var db = new SQL.Database(filebuffer);
  var contents = db.exec("SELECT TOP 10 FROM telemetria");
});
console.log(contents)
document.getElementById("test").innerHTML = contents

// xhr.send();