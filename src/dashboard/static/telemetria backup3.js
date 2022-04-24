lnk = "ws://127.0.0.1:5004"

console.log(lnk)

var connection = new WebSocket(lnk);

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

json_recv = getJSON(lnk)

console.log(json_recv);