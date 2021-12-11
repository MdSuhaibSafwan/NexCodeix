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
    if (data.msg_type != "SRJ"){
        return null;
    };
    
    var class_joined_user_id = data.id;
    var user = data.user;

    var table = document.getElementById("student-joining-table");
    
    var tBody = document.createElement("tbody");
    var tR = document.createElement("tr");
    var th1 = document.createElement("th");
    th1.setAttribute("scope", "row");
    
    var td1 = document.createElement("td");
    var td2 = document.createElement("td");
    var td3 = document.createElement("td");
    var td4 = document.createElement("td");

    td1.textContent = `${user.first_name}`;
    td2.textContent = `${user.email}`;

    var btn1 = document.createElement("a");
    btn1.setAttribute("class", "btn btn-outline-primary");
    btn1.textContent = "Accept";

    var url = `/batch/user/class/make_join/${class_joined_user_id}/`;

    var btn2 = document.createElement("a");
    btn2.setAttribute("class", "btn btn-outline-danger");
    btn2.textContent = "Reject";

    btn1.setAttribute("data-url", url);
    btn2.setAttribute("data-url", url+"?type=reject");

    td3.appendChild(btn1);
    td4.appendChild(btn2);

    tR.appendChild(th1);
    tR.appendChild(td1);
    tR.appendChild(td2);
    tR.appendChild(td3);
    tR.appendChild(td4);

    tBody.appendChild(tR);
    table.appendChild(tBody);

    btn1.addEventListener("click", (event) => {
        var url = btn1.getAttribute("data-url");
        triggerForJoining(event, url, class_joined_user_id);
    });

    btn2.addEventListener("click", (event) => {
        var url = btn2.getAttribute("data-url");
        return triggerForJoining(event, url, class_joined_user_id);
    });
};


function triggerForJoining(event, url, cj_user_id){
    event.preventDefault();
    
    fetch(url, {
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
    })

    .then((resp) => {
        console.log(resp);
        if (resp.status == 200){
            socket.send(JSON.stringify({
                data: "UJS",
                class_joined_user_id: cj_user_id,
                msg_type: "UJS"
            })
            );
        return resp.json();
        };
    })
    .then((data) => {
        if (data == null){
            return 
        }
        if (data.user == "ACCEPTED"){
            console.log("Joined");
        };

        if (data.user == "NOT JOINED"){
            console.log("Not Joined");
        }
    })
};

socket.onerror = (event) =>{
    console.log(event);
};

socket.onclose = (event) =>{
    console.log(event);
};