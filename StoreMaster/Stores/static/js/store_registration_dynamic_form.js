$(document).ready(function () {
    var currentManagerChoice = "";
    var currentFirstName = "";
    var currentLastName = "";
    var currentAddress = "";
    var currentLineTwo = "";
    var currentCity = "";
    var currentState = "";
    var currentZip = "";
    var currentUsername = "";
    var currentPassword  = "";
    var currentOtherInfo = "";
    var currentBirthday = "";

    // var new_manager_form_open = false;

    const managerSelector = $("[name='manager_selector']");
    const firstName = $("[name='first_name']");
    const lastName = $("[name='last_name']");
    const address = $("[name='address']");
    const lineTwo = $("[name='line_two']");
    const city = $("[name='city']");
    const state = $("[name='state']");
    const zip = $("[name='zip']");
    const username = $("[name='username']");
    const password = $("[name='password']");
    const otherInfo = $("[name='other_info']");
    const birthday = $("[name='birthday']");

    const existingManagerDiv = $('#register_existing_manager_div');
    const newManagerDiv = $('#register_new_manager_div');

    if(loadNewManagerFirst) {
        existingManagerDiv.hide();
    }
    else {
        newManagerDiv.hide();
    }
    $('#add_new_manager_form_button').click(function() {
        
        currentManagerChoice = managerSelector.val();
        existingManagerDiv.hide();
        newManagerDiv.show();
        
        firstName.val(currentFirstName);
        lastName.val(currentLastName);
        address.val(currentAddress);
        lineTwo.val(currentLineTwo);
        city.val(currentCity);
        state.val(currentState);
        zip.val(currentZip);
        username.val(currentUsername);
        password.val(currentPassword);
        otherInfo.val(currentOtherInfo);
        birthday.val(currentBirthday);

    });

    $('#return_button').click(function() {
        currentFirstName = firstName.val();
        currentLastName = lastName.val();
        currentAddress = address.val();
        currentLineTwo = lineTwo.val();
        currentCity = city.val();
        currentState = state.val();
        currentZip = zip.val();
        currentUsername = username.val();
        currentPassword = password.val();
        currentOtherInfo = otherInfo.val();
        currentBirthday = birthday.val();
        
        existingManagerDiv.show();
        newManagerDiv.hide();
        managerSelector.val(currentManagerChoice);
    });

});