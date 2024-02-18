var attempt_login = function() {
    let username = $("#username-entry").val();
    let password = $("#password-entry").val();

    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    
    let login_data = {
        "username":username,
        "password":password,
        csrfmiddlewaretoken: csrftoken
    };

    fetch('login_employee', {
        method:'POST',
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(login_data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('network response was not ok');
        } else if (response.redirected) {
            window.location.href = response.url;
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        $("#message-space").show();
        $("#message-space").text(data.message);
    })
    .catch(error => {
        console.error('Error:',error);
    });


    console.log("Attempting login..");
}

$(document).ready(function() {
    //Hide the message area
    $("#message-space").hide();

    //Event Listeners
    $(".employee-login-fields").on("input",function() {
        $("#message-space").hide();    
    });

    $("#employee-login-form").submit(function(event) {
        event.preventDefault();

        var username = $("#username-entry").val();
        var password = $("#password-entry").val();

        //Verify user input for credentials
        if (username.trim() === "" || password.trim() === "") {
            alert("Please enter a username and password");
        } else if (username.trim() === "") {
            alert("Please enter a username");
        } else if (password.trim() === "") {
            alert("Please enter a password");
        } else {
            attempt_login();
        }

    })
});