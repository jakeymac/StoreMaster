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
        var account_data = data.account_data;
        $("#store-id-input").val(account_data.store.store_id);
        $("#customer-id-input").val(customer_id);

        $("#customer-name-header").text(account_data.first_name + account_data.last_name);
        if (account_data.address) {
            $("#customer-address-p").text("Address: " + account_data.address);
        }
        if (account_data.line_two) {
            $("#customer-line-two-p").text("Address 2: " + account_data.line_two);
        }

        $("#customer-username-p").text("Username: " + account_data.username);
        $("#customer-birthday-p").text("Birthday: " + account_data.birthday);
        $("#customer-other-information-p").html("Other information: <br>" + account_data.other_information);

    });
}

function load_listeners() {
    $("#edit-customer-button").on("click", function() {
        $("#open-edit-customer-form").submit();
    })
    

}

$(document).ready(function() {
    load_data();
    load_listeners();
})