function load_product_data() {
    console.log("Loading product data");
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(store_id, {
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
    console.log("Loading product data listeners");
}

$(document).ready(function() {
    load_product_data();
    load_listeners();
});