lnk = "ws://127.0.0.1:5004"

// Telemetria global variables.
var truck_id;
var evento;
var timestamp;
var rotacao;
var bau;
var janela;
var conectado;
var estaBloqueiado;
var bloqueiomanual;
var latitude;
var longitude;

// Macro global variables
var truck_id_2;
var evento_2;
var timestamp_2;
var latitude_2;
var longitude_2;
var mensagem;

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
    //alert(`[message] Data received from server: ${event.data}`);
    //Colocar aqui as variaveis a serem mostradas no HTML.
    var json_recv = JSON.parse(event.data);
    console.log(json_recv);
    if (json_recv['evento'] == "Telemetria"){
        var truck_id = json_recv['truck_id'];
        var evento = json_recv['evento'];
        var timestamp = json_recv['timestamp'];
        var rotacao = json_recv['rotacao'];
        var bau = json_recv['bau'];
        var janela = json_recv['janela'];
        var conectado = json_recv['conectado'];
        var estaBloqueiado = json_recv['estaBloqueiado'];
        var bloqueiomanual = json_recv['bloqueiomanual'];
        var latitude = json_recv['latitude'];
        var longitude = json_recv['longitude'];
        document.getElementById('latitude').innerHTML = latitude;
        document.getElementById('longitude').innerHTML = longitude;
        document.getElementById('timestamp').innerHTML = timestamp;
        console.log(evento);
        console.log(timestamp);
    }
    if (json_recv['evento'] == "Macro"){
        var truck_id = json_recv['truck_id'];
        var evento_2 = json_recv['evento'];
        var timestamp_2 = json_recv['timestamp'];
        var latitude_2 = json_recv['latitude'];
        var longitude_2 = json_recv['longitude'];
        var mensagem = json_recv['mensagem'];
        console.log(evento_2);
        console.log(timestamp_2);
        console.log(mensagem);
    }
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

function requestRoutineTelemetria(){
    sendMessage("telemetria", connection);
    //sendMessage("macro", connection);
}

function requestRoutineMacro(){
    sendMessage("macro", connection);
    //sendMessage("macro", connection);
}

function pureWait(){
    console.log("Waiting...")
}

setInterval(requestRoutineTelemetria, 10000);
setInterval(pureWait,5000);
setInterval(requestRoutineMacro, 10000);
