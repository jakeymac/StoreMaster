function load_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        
    })
}

function load_listeners() {

}

$(document).ready(function() {
    load_data();
    load_listeners();
});