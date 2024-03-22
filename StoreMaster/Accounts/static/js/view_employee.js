var employee_data;
function load_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    console.log(employee_id);
    fetch(`/api/account/${employee_id}`, {
        method: "GET",
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
        employee_data = data.account_data;
        $("#name-header").text(employee_data.first_name + " " + employee_data.last_name);
        $("#address-p").html(`<strong>Address:</strong> ${employee_data.address}`);
        $("#city-p").html(`<strong>City:</strong> ${employee_data.city}`);
        $("#state-p").html(`<strong>State:</strong> ${employee_data.state}`);
        $("#zip-p").html(`<strong>Zip:</strong> ${employee_data.zip}`);
        if (employee_data.email) {
            $("#email-p").html(`<strong>Email:</strong> ${employee_data.email}`);
        }
       if(employee_data.other_information) {
            $("#other-info-p").html(`<strong>Other Information:</strong> ${employee_data.other_information}`);
       }
        $("#birthday-p").html(`<strong>Birthday:</strong> ${employee_data.birthday}`);
        $("#account-type-p").html(`<strong>Account Type:</strong> ${employee.account_type}`);
    })
}

function load_listeners() {
    $("#edit-information-button").on("click", function() {
        window.location.href = `/edit_employee/${employee_data.user.id}`; //Change this later when updating the views page I dont' want this ot need the employee type
    });

    $("#back-to-portal-button").on("click", function() {
        window.location.href = `/manage_store/${employee_data.store.store_id}`;
    });
}

$(document).ready(function() {
    load_data();
    load_listeners();
});