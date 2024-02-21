var storeName = "";
var storeAddress = "";
var storeLineTwo = "";
var storeCity = "";
var storeState = "";
var storeZip = "";

var chosen_manager_id = null;
var chosen_manager_info = null;
var chosen_manager_stock_notifications = false;

var new_manager_first_name = "";
var new_manager_last_name = "";
var new_manager_address = "";
var new_manager_line_two = "";
var new_manager_city = "";
var new_manager_state = "";
var new_manager_zip = "";
var new_manager_username = "";
var new_manager_password = "";
var new_manager_email_address = "";
var new_manager_other_info = "";
var new_manager_birthday = "";
var new_manager_stock_notifications = null;

function load_forms() {
    //Add event and form listeners

    $(".form-required-entry").each(function (){
        $(this).on('input', function() {
            $(this).removeClass('empty-highlight');
            $("#message-space").text(" ");
        })
    });

    $("#store_registration_form_1").submit(function(event) {
        event.preventDefault();
        var complete = true;
        $(".form-1-input.form-required-entry").each(function() {
            if ($(this).val().trim() === "") {
                $(this).addClass('empty-highlight');
                $("#message-space").text("Make sure all fields are filled in");
                complete = false;
            }
        });

        if(complete) {
            console.log("Next page time");
            storeName = $("#store-name-entry").val();
            storeAddress = $("#store-address-entry").val();
            storeLineTwo = $("#store-line-two-entry").val();
            storeCity = $("#store-city-entry").val();
            storeState = $("#store-state-entry").val();
            storeZip = $("#store-zip-entry").val();

            console.log("Time for zip: ", storeZip);

            let csrftoken = $("input[name=csrfmiddlewaretoken]").val();    
        
            requestData = {
                "step": 1,
                "store_name": storeName,
                "store_address": storeAddress,
                "store_line_two": storeLineTwo,
                "store_city": storeCity,
                "store_state": storeState,
                "store_zip": storeZip,
                csrfmiddlewaretoken: csrftoken
            };

            fetch('register_store', {
                method:'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(requestData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                var valid = data["valid"]
                if (valid == 1) {
                    load_step_2();
                } else {
                    $("#message-space").text("A store with that name already exists at that location");
                }
            })
        }
    });

    $("#switch-to-new-button").on("click", function() {
        load_step_3();
        $(".form-required-entry").each(function (){
            $(this).removeClass('empty-highlight');
            $("#message-space").text(" ");
        });
    });

    $("#store_registration_form_2").submit(function(event) {
        event.preventDefault();
        chosen_manager_id = $("#manager_selector").val();
        console.log("Step 2 beginning: ", chosen_manager_id);
        let csrftoken = $("input[name=csrfmiddlewaretoken]").val();

        if (chosen_manager_id) {
            console.log("Selected");

            var requestData = {
                "id":chosen_manager_id,
                "step": 2,
                csrfmiddlewaretoken: csrftoken
            };

            fetch('register_store', {
                method:'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                }, 
                body: JSON.stringify(requestData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                chosen_manager_info = data.manager;
                chosen_manager_stock_notifications = $("#existing_manager_stock_notifications_entry").prop('checked');
                
                load_final_confirmation("existing");
            })
            .catch(error => {
                console.error('Error:', error);
            })
        } else {
            $("#manager_selector").addClass('empty-highlight');
            $("#message-space").text("Select a manager");
        }
    });

    $("#switch-to-existing-button").on("click", function() {
        load_step_2();
        $(".form-required-entry").each(function (){
            $(this).removeClass('empty-highlight');
            $("#message-space").text(" ");
        });
    });

    $("#store_registration_form_3").submit(function(event) {
        event.preventDefault();
        var complete = true;
        $(".form-3.form-required-entry").each(function() {
            console.log("blah");
            console.log($(this).attr('id'));
            if ($(this).val().trim() === "") {
                $(this).addClass('empty-highlight');
                $("#message-space").text("Make sure all fields are filled in");
                complete = false;
            }
        });
        if (complete) {
            
            let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
            new_manager_first_name = $("#new_manager_first_name_entry").val();
            new_manager_last_name = $("#new_manager_last_name_entry").val();
            new_manager_address = $("#new_manager_address_entry").val();
            new_manager_line_two = $("#new_manager_line_two_entry").val();
            new_manager_city = $("#new_manager_city_entry").val();
            new_manager_state = $("#new_manager_state_entry").val();
            new_manager_zip = $("#new_manager_zip_entry").val();
            new_manager_username = $("#new_manager_username_entry").val();
            new_manager_password = $("#new_manager_password_entry").val();
            new_manager_email_address = $("#new_manager_email_address_entry").val();
            new_manager_other_info = $("#new_manager_other_info_entry").val();
            new_manager_birthday = $("#new_manager_birthday_entry").val();
            new_manager_stock_notifications = $("#new_manager_stock_notifications_entry").prop('checked');
            
            var newManagerData = {"email_address": new_manager_email_address,
                                    "username": new_manager_username,
                                    "step": 3,
                                    csrfmiddlewaretoken: csrftoken};

            fetch('register_store', {
                method:'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(newManagerData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data["valid"] == 0) {
                    console.log("Valid");
                    load_final_confirmation("new");
                }
                else if (data["valid"] == 1) {
                    console.log("Not valid");
                    $("#message-space").text("Sorry, an account with that username already exists");
                }
                else if (data["valid"] == 2) {
                    console.log("Not valid");
                    $("#message-space").text("Sorry, an account with that email already exists");
                }
                else if (data["valid"] == 3) {
                    console.log("Not valid");
                    $("#message-space").text("Sorry, an account with that username and that email already exists");
                }
                    
            })
            .catch(error => {
                console.error("Error: ", error);
            });
            
            console.log("Form 3");
        }
    });

    // Load Data
    fetch('get-all-available-managers', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Managers");
        //console.log(data);
        var managers = data["managers"]
        if (managers) {
            for (var key in managers) {
                var manager = managers[key];
                $("#manager_selector").append(`<option value="${manager.id}">${manager.manager_name}</option>`);
                console.log(managers[key]);
            }
        }
        else {
            $("#manager_selector").append(`<option value="-99999">No available managers found</option>`);
        }
    })
    .catch(error => {
        console.error("Error", error);
    });

}


function load_step_1() {
    $("#store-registration-container-2").hide();
    $("#store-registration-container-3").hide();
    $("#store-registration-container-4").hide();
    $("#store-registration-container-1").show();


}
function load_step_2() {

    // OK BIG COMMENT HERE
    // MAKE SURE THAT A MANAGER ISNT REGISTERED TO A STORE ALREADY FOR THE DROP DOWN 
    // SELECTOR MAYBE IDK
    $("#store-registration-container-1").hide();
    $("#store-registration-container-3").hide();
    $("#store-registration-container-4").hide();
    $("#store-registration-container-2").show();
    

    

}
        


function load_step_3() {
    console.log("Loading form 3");
    $("#store-registration-container-1").hide();
    $("#store-registration-container-2").hide();
    $("#store-registration-container-4").hide();
    $("#store-registration-container-3").show();

    
}

function load_final_confirmation(managerType) {
    console.log("Loading form 4");
    $("#store-registration-container-2").hide();
    $("#store-registration-container-3").hide();
    $("#store-registration-container-4").show();

    $("#store-name-confirmation-label").html(`Store Name: <strong>${storeName}</strong>`);
    var storeAddressLabelText = `Store Address: <strong>${storeAddress} `;
    if (storeLineTwo) { 
        storeAddressLabelText += `${storeLineTwo} `;
    }
    $("#store-address-confirmation-label").html(storeAddressLabelText);
    $("#store-city-confirmation-label").html(`Store City: <strong>${storeCity}</strong`);
    $("#store-state-confirmation-label").html(`Store State: <strong>${storeState}</strong>`);
    $("#store-zip-confirmation-label").html(`Store Zip: <strong>${storeZip}</strong>`);

    var newStoreData = {"name":storeName,
                        "address":storeAddress,
                        "line_two":storeLineTwo,
                        "city": storeCity,
                        "state": storeState,
                        "zip": storeZip};
    
    var requestData = {};
    var new_manager_info = {};
    $("#confirm-manager-information-container").empty();
    if (managerType === "existing") {

        console.log("Pre-existing manager chosen");
        $("#confirm-manager-information-container").append(`<label>Manager name: <strong>${chosen_manager_info.first_name} ${chosen_manager_info.last_name}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Manager email: <strong>${chosen_manager_info.email_address}</strong></label><br>`);

        var stock_label = "Off";
        if (chosen_manager_stock_notifications) {
            stock_label = "On";
        }
        
        $("#confirm-manager-information-container").append(`<label>Stock Notifications: <strong>${stock_label}</strong></label>`);
        $("#confirm-manager-information-container").append(`<button class="manager-edit-button">Edit</button>`);

        requestData = {"manager_info": chosen_manager_info,
                       "stock_notifications": chosen_manager_stock_notifications,
                       "id":chosen_manager_id,
                       "manager_type":"pre-existing"};

        $(".manager-edit-button").on("click", function() {
            load_step_2();
        });
        
    } else { //New manager chosen
        console.log("New manager chosen"); 

        $("#confirm-manager-information-container").append(`<label>Manager Name: <strong>${new_manager_first_name} ${new_manager_last_name}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Manager Address: <strong>${new_manager_address}</strong></label><br>`);
        if (new_manager_line_two) {
            $("#confirm-manager-information-container").append(`<label>Line Two: <strong>${new_manager_line_two}</strong></label><br>`);
        }
        $("#confirm-manager-information-container").append(`<label>City: <strong>${new_manager_city}</strong></label><br>`);
        
        $("#confirm-manager-information-container").append(`<label>State: <strong> ${new_manager_state}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Zip: <strong>${new_manager_zip}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Username: <strong>${new_manager_username}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Other Info: <strong>${new_manager_other_info}</strong></label><br>`);
        $("#confirm-manager-information-container").append(`<label>Birthday: <strong>${new_manager_birthday}</strong></label><br>`);
        var stock_label = "Off";
        if (new_manager_stock_notifications) {
            stock_label = "On";
        }
        $("#confirm-manager-information-container").append(`<label>Stock Notifications: <strong>${stock_label}</strong></label>`);
        $("#confirm-manager-information-container").append(`<button class="manager-edit-button">Edit</button>`);

        new_manager_info = {"first_name":new_manager_first_name,
                            "last_name":new_manager_last_name,
                            "address":new_manager_address,
                            "line_two":new_manager_line_two,
                            "city":new_manager_city,
                            "state":new_manager_state,
                            "zip":new_manager_zip,
                            "username":new_manager_username,
                            "password":new_manager_password,
                            "email":new_manager_email_address,
                            "other_info":new_manager_other_info,
                            "birthday":new_manager_birthday,
                            "stock_notifications":new_manager_stock_notifications};

        requestData = {"manager_info": new_manager_info, "manager_type":"new"};

        $(".manager-edit-button").on("click", function() {
            console.log("Edit manager button pressed");
            load_step_3();
        });
    }

    $("#confirmation-store-edit-button").on("click", function() {
        load_step_1();
    })

    requestData["store_info"] = newStoreData;
    requestData["step"] = 4
    
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    requestData["csrfmiddlewaretoken"] = csrftoken;

    $("#confirm-info-button").on("click", function() {
        //TODO here could be changed to make one final check on the information,
        //to make sure nothing has changed in the database at the last minute
        
        fetch('register_store', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('network response was not ok');
            } 
            return response.json();
        })
        .then(data => {
            //TODO next step here, go back to view and save the store and manager info 
            //if needed in the database, then return a valid message here or an invalid message
            //then add edit button functionality - show specific manager div depending on choice
            console.log("data");
            if (data["confirmation"]) {
                window.location.href = `manage_store/${data["store_id"]}`;
                
            } else {
                
                console.log(data["messages"]);
                var messages_string = "";
                data["messages"].forEach(function(message) {
                    messages_string += `${message}\n`;
                });
                $("#message-space").text(messages_string);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        })
    })
}



$(document).ready(function() {
    $("#message-space").text(" ");
    load_forms();
    load_step_1();
});