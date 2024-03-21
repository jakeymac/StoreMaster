function load_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(window.location.href, {
        method: "POST", 
        headers: {
            "Content-Type": "appliation/json",
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
        for (var store in data.stores) {
            var id = data.stores[store][0];
            var name = data.stores[store][1];
            $("#store-selector").append(`<option value=${id}>${name}</option>`);
        }
        
        for (var employee in data.employees) {
            var id = data.employees[employee][0];
            var name = data.employees[employee][1];
            $("#employee-selector").append(`<option value=${id}>${name}</option>`);
        }

        for (var customer in data.customers) {
            var id = data.customers[customer][0];
            var name = data.customers[customer][1];
            $("#customer-selector").append(`<option value=${id}>${name}</option>`);
        }
    })
}

function load_listeners() {
    $("#select-store-button").on("click", function() {
        if ($("store-selector").val() != "") {
            window.location.href = `/manage_store/${$("#store-selector").val()}`;
        }
    });

    $("#select-employee-button").on("click", function() {
        if ($("#employee-selector").val() != "") {
            window.location.href = `/view_employee/${$("#employee-selector").val()}`;
        }
    });

    $("#select-customer-button").on("click", function() {
        if ($("#customer-selector").val() != "") {
            window.location.href = `/employee_view_customer/${$("#customer-selector").val()}`;
        }
    });

    $("#logout-employee-button").on("click", function() {
        window.location.href = `/logout_employee`;
    });
}

$(document).ready(function() {
    load_data();
    load_listeners();
});