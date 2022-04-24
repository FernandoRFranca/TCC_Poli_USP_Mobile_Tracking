lnk = "ws://127.0.0.1:5004"

function sendMessage(msg, ws){
    // Wait until the state of the socket is not ready and send the message when it is...
    waitForSocketConnection(ws, function(){
        console.log("message sent!!!");
        ws.send(msg);
    });
}

// Make the function wait until the connection is made...
function waitForSocketConnection(socket, callback){
    setTimeout(
        function () {
            if (socket.readyState === 1) {
                console.log("Connection is made")
                if (callback != null){
                    callback();
                }
            } else {
                console.log("wait for connection...")
                waitForSocketConnection(socket, callback);
            }

        }, 5); // wait 5 milisecond for the connection...
}

console.log(lnk)

var connection = new WebSocket(lnk)

waitForSocketConnection(connection);

connection.onmessage = function(event) {
    alert(`[message] Data received from server: ${event.data}`);
  };
  
connection.onclose = function(event) {
if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
} else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died');
}
};
  
connection.onerror = function(error) {
alert(`[error] ${error.message}`);
};

sendMessage("telemetria", connection);
