var employee_data;
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
        employee_data = data.employee;
        $("#name-header").text(data.employee.first_name + " " + data.employee.last_name);
        $("#address-p").html(`<strong>Address:</strong> ${data.employee.address}`);
        $("#city-p").html(`<strong>City:</strong> ${data.employee.city}`);
        $("#state-p").html(`<strong>State:</strong> ${data.employee.state}`);
        $("#zip-p").html(`<strong>Zip:</strong> ${data.employee.zip}`);
        $("#email-p").html(`<strong>Email:</strong> ${data.employee.email}`);
        $("#other-info-p").html(`<strong>Other Information:</strong> ${data.employee.other_information}`);
        $("#birthday-p").html(`<strong>Birthday:</strong> ${data.employee.birthday}`);
        $("#account-type-p").html(`<strong>Account Type:</strong> ${data.account_type}`);
    })
}

function load_listeners() {
    $("#edit-information-button").on("click", function() {
        window.location.href = `/edit_employee/${employee_data.id}/${employee_data.account_type}`; //Change this later when updating the views page I dont' want this ot need the employee type
    });

    $("#back-to-portal-button").on("click", function() {
        window.location.href = `/manage_store/${employee_data.store_id}`;
    });
}

$(document).ready(function() {
    load_data();
    load_listeners();
});