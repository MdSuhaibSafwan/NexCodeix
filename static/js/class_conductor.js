var currUserToken = user_token;
var classId = class_obj_id;
console.log(currUserToken, classId);

var loc = location;
console.log(loc);

var ws = "ws:";

if (loc.protocol == "https:") ws = "wss:"
var url = `${ws}//${loc.host}/batch/class/room/?token=${currUserToken}&class_id=${classId}`;
console.log(url);

var socket = new WebSocket(url);

socket.onopen = (event) =>{
    console.log(event);
};

socket.onmessage = (event) =>{
    var data = JSON.parse(event.data);
    console.log(data);
};

socket.onerror = (event) =>{
    console.log(event);
};

socket.onclose = (event) =>{
    console.log(event);
};