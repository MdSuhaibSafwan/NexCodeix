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
}
const csrftoken = getCookie('csrftoken');

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
