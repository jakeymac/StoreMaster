function load_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(`/api/account/${employee_id}`, {
        method: 'GET',
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
        
        var employee_data = data.account_data;
        if(employee_data.account_type == "customer") {
            window.location.href = `/view_customer/${employee_data.user.id}`;
        } else {
            $("#first-name-input").val(employee_data.first_name);
            $("#last-name-input").val(employee_data.last_name);
            $("#email-address-input").val(employee_data.email_address);
            $("#address-input").val(employee_data.address);
            $("#line-two-input").val(employee_data.line_two);
            $("#city-input").val(employee_data.city);
            $("#state-input").val(employee_data.state);
            $("#zip-input").val(employee_data.zip);
            $("#username-input").val(employee_data.username);
            $("#password-input").val(employee_data.password);
            $("#other-information-input").val(employee_data.other_information);
            if(employee_data.birthday) {
                var parts_of_birthday = employee_data.birthday.split("-");
                var month = parts_of_birthday[0];
                var day = parts_of_birthday[1];
                var year = parts_of_birthday[2];
                var reformatted_birthday = `${year}-${month}-${day}`;
                $("#birthday-input").val(reformatted_birthday);
            }
            $("#account-type-selector").val(employee_data.account_type);
            
            if (employee_data.account_type == "manager") {
                $("#stock-notifications-div").show();
                $("#stock-notifications-checkbox").prop("checked", employee_data.stock_notifications);
            }
            fetch(`/api/store`, {
                method: 'GET',
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
                var all_stores = data.stores;
                for (var store in all_stores) {
                    var option = $('<option>', {
                        value: all_stores[store].store_id,
                        text: all_stores[store].store_name
                    });
                    if(all_stores[store].store_id == employee_data.store.store_id) {
                        option.prop('selected', true);
                    }
        
                    $("#store-selector-input").append(option);
                }
            });
        }
    });
        
    
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
        if ($("#zip-input").val()) {
            var zip = $("#zip-input").val();
        } else {
            var zip = null;
        }
        var username = $("#username-input").val();
        var password = $("#password-input").val();
        var store_id = $("#store-selector-input").val();
        var other_information = $("#other-information-input").val();
        var birthday = $("#birthday-input").val();
        var account_type = $("#account-type-selector").val();
        var stock_notifications = $("#stock-notifications-checkbox").prop("checked");

        var user_data = {"id": employee_id,
                         "username": username,
                         "password": password,
                         "email": email_address}

        var employee_data = {"employee_id": employee_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email_address": email_address,
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
        fetch('/api/account', {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({user: user_data,
                                  account_data: employee_data})        
        })
        .then(response => {
            console.log(response);
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