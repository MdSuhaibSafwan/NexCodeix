const sendQueryUrl = queryUrl;
console.log(sendQueryUrl);
var form = document.querySelector("#contactus-form");

form.addEventListener('submit', (event) => {
  console.log("Event ", event);
  event.preventDefault();
  var inputs = event.target.getElementsByTagName("input");
  console.log(inputs);
  var data = {};
  for (input of inputs){
    let name = input.getAttribute("id");
    let val = input.value;
    data[name] = val;
  };

  let textField = event.target.getElementsByTagName("textarea")[0];
  data[textField.getAttribute("name")] = textField.value;

  return sendMessageDataToServer(data, event.target);

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


const csrftoken = getCookie('csrftoken');

function sendMessageDataToServer(data, form){
    console.log(data);

    stringifyData = JSON.stringify(data)

    let csrftoken = getCookie('csrftoken');
    let response = fetch(sendQueryUrl, {
        method: 'POST',
        body: stringifyData,
        headers: { 
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json',
          "X-CSRFToken": csrftoken 
        },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((data) => {
        console.log(data);
        var respStatus = data.status;
        if (respStatus == 200){
          var msgDiv = document.querySelector("#query-response-message");
          var sentMsgDiv = msgDiv.querySelector(".sent-message");
          sentMsgDiv.classList.add("d-block");
        };
      })
      .then(() => {
        console.log("Form", form);
        form.reset();
      })



}

