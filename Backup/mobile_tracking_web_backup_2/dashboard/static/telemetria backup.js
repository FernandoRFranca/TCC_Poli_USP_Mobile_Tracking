var xhr = new XMLHttpRequest();
// For example: https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite
xhr.open('GET', 'telemetria.db', true);
xhr.responseType = 'arraybuffer';

xhr.onload = e => {
  var uInt8Array = new Uint8Array(this.response);
  var db = new SQL.Database(uInt8Array);
  var contents = db.exec("SELECT TOP 10 FROM telemetria");
  // contents is now [{columns:['col1','col2',...], values:[[first row], [second row], ...]}]
};

document.getElementById("test").innerHTML = contents

// xhr.send();