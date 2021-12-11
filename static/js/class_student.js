var curr_user = currentUser;
console.log(curr_user);

var form = document.getElementById("join_form");
form.addEventListener("submit", (event) => {
    event.preventDefault();
    var val = form.getElementsByTagName("input")[1].value;
    var url = view_url;
    console.log(url);
    fetch(url, {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        "body": JSON.stringify({
            "joining": true,
            "is_ajax": true,
        })
    })
    .then((resp) => {
        return resp.json();
    })           
    .then((data) => {
        console.log(data);
    }) 
});


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
    console.log(event);
    var data = JSON.parse(event.data);
    var user_joining_lst = ["UJS", "UNJ"]
    if (data.msg_type in user_joining_lst && data.user == curr_user){
        console.log("Making to Joined From Pending");
    };   
};

socket.onerror = (event) =>{
    console.log(event);
};

socket.onclose = (event) =>{
    console.log(event);
};


