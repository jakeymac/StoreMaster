var employee_id;
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
        var employee_info = data.employee_info;
        employee_id = employee_info.id;

        $("#first-name-input").val(employee_info.first_name);
        $("#last-name-input").val(employee_info.last_name);
        $("#email-address-input").val(employee_info.email);
        $("#address-input").val(employee_info.address);
        $("#line-two-input").val(employee_info.line_two);
        $("#city-input").val(employee_info.city);
        $("#state-input").val(employee_info.state);
        $("#zip-input").val(employee_info.zip);
        $("#username-input").val(employee_info.username);
        $("#password-input").val(employee_info.password);

        for (var store in data.all_stores) {
            var option = $('<option>', {
                value: data.all_stores[store].id,
                text: data.all_stores[store].name
            });

            if(data.all_stores[store].id == employee_info.store_id) {
                option.prop('selected', true);
            }

            $("#store-selector-input").append(option);
        }

        $("#other-information-input").val(employee_info.other_information);
        $("#birthday-input").val(employee_info.birthday);
        $("#account-type-selector").val(employee_info.account_type);
        
        if (employee_info.account_type == "manager") {
            $("#stock-notifications-div").show();
            $("#stock-notifications-checkbox").prop("checked", employee_info.stock_notifications);
        }

       
        
    })
}

function load_listeners() {
    $("#save-changes-button").on("click", function() {
        var first_name = $("#first-name-input").val();
        var last_name = $("#last-name-input").val();
        var email_address = $("#email-address-input").val();
        var address = $("#address-input").val();
        var line_two = $("#line-two-input").val();
        var city = $("#city-input").val();
        var state = $("#state-input").val();
        var zip = $("#zip-input").val();
        var username = $("#username-input").val();
        var password = $("#password-input").val();
        var store_id = $("#store-selector-input").val();
        var other_information = $("#other-information-input").val();
        var birthday = $("#birthday-input").val();
        var account_type = $("#account-type-selector").val();
        var stock_notifications = $("#stock-notifications-checkbox").prop("checked");

        var employee_data = {"employee_id": employee_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email_address,
                            "address": address,
                            "line_two": line_two,
                            "city": city,
                            "state": state,
                            "zip": zip,
                            "username": username,
                            "password": password,
                            "store_id": store_id,
                            "other_information": other_information,
                            "birthday": birthday,
                            "account_type": account_type,
                            "stock_notifications": stock_notifications}

        let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        fetch('/api/edit_employee', {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(employee_data)        
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update employee');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error updating employee:', error);
        });

    });

    $("#back-button").on("click", function() {
        window.location.href = `/view_employee/${employee_id}`;
    })

    
}

$(document).ready(function() {
    load_data();
    load_listeners();
});