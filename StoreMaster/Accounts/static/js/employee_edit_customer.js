let account_data;
function load_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(`/api/account/${customer_id}`, {
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
        account_data = data.account_data;
        $("#first-name-input").val(account_data.first_name);
        $("#last-name-input").val(account_data.last_name);
        $("#email-address-input").val(account_data.email_address);
        $("#address-input").val(account_data.address);
        $("#line-two-input").val(account_data.line_two);
        $("#city-input").val(account_data.city);
        $("#state-input").val(account_data.state);
        $("#zip-input").val(account_data.zip);
        $("#other-information-input").val(account_data.other_information);
        if(account_data.birthday) {
            var parts_of_birthday = account_data.birthday.split("-");
            var month = parts_of_birthday[0];
            var day = parts_of_birthday[1];
            var year = parts_of_birthday[2];
            var reformatted_birthday = `${year}-${month}-${day}`;
            $("#birthday-input").val(reformatted_birthday);
        }
    })
}

function load_listeners() {
    $("#save-info-button").on("click", function() {
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
        var other_information = $("#other-information-input").val();
        var birthday = $("#birthday-input").val();

        var user_data = {"id": customer_id,
                         "email": email_address};

        var customer_data ={"customer_id": customer_id,
                            "store_id": account_data.store.store_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email_address": email_address,
                            "address": address,
                            "line_two": line_two,
                            "city": city,
                            "state": state,
                            "zip": zip,
                            "other_information": other_information,
                            "account_type": "customer",
                            "birthday": birthday}

        let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
        fetch(`/api/account`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({user: user_data,
                                  account_data: customer_data})
        })
        .then(response => {
            console.log(response);
            if (response.status >= 200 && response.status < 300) {
                return response.json()
            } else {
                return response.json().then(data => {
                    console.log("Resposne section");
                    $("#messages-p").show();
                    var messages_text = "";
                    for (var message in data.messages) {
                        console.log(data.messages[message]);
                        messages_text += data.messages[message] + "\n";
                        
                    }
                    $("#messages-p").text(messages_text);
                    console.log(data.messages);
                });
            }
        })
        .then(data => {
            Swal.fire({
                icon:'info',
                title:'Information Saved',
                text:'Account information succesfully saved',
                timer: 3000,
                timerProgressBar: false,
                customClass: {
                    popup: 'saved-successfully-alert'
                }
            });
            setTimeout(function() {
                $("#back-to-employee-info-form").submit();
            }, 3000);
        })
        .catch(error => {
            console.error('Error updating account information', error);
        });

    })
}

$(document).ready(function() {
    load_data();
    load_listeners();
})