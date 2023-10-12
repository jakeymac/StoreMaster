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
    
    $('#add_new_manager_form_button').click(function() {
        $('#select_existing_manager').hide();
        $('#register_new_manager').show();
        
        currentManagerChoice = $("[name='manager']").val();
        $("[name='first_name']").val(currentFirstName);
        $("[name='last_name']").val(currentLastName);
        $("[name='address']").val(currentAddress);
        $("[name='line_two']").val(currentLineTwo);
        $("[name='city']").val(currentCity);
        $("[name='state']").val(currentState);
        $("[name='zip']").val(currentZip);
        $("[name='username']").val(currentUsername);
        $("[name='password']").val(currentPassword);
        $("[name='other_info']").val(currentOtherInfo);
        $("[name='birthday']").val(currentBirthday);

        toggleRequiredFields();
    });

    $('#return_button').click(function() {
        $('#register_new_manager').hide();
        $('#select_existing_manager').show();

        $("[name='manager']").val(currentManagerChoice);
        currentFirstName = $("[name='first_name']").val();
        currentLastName = $("[name='last_name']").val();
        currentAddress = $("[name='address']").val();
        currentLineTwo = $("[name='line_two']").val();
        currentCity = $("[name='city']").val();
        currentState = $("[name='state']").val();
        currentZip = $("[name='zip']").val();
        currentUsername = $("[name='username']").val();
        currentPassword = $("[name='password']").val();
        currentOtherInfo = $("[name='other_info']").val();
        currentBirthday = $("[name='birthday']").val();

        toggleRequiredFields();
    });

    function toggleRequiredFields() {
        $("[name='manager']").prop("required", function(i, required) {
            return !required;
        });
        
        $("[name='first_name']").prop("required", function(i, required) {
            return !required;
        });
        
        $("[name='last_name']").prop("required", function(i, required) {
            return !required;
        });
        
        $("[name='username']").prop("required", function(i, required) {
            return !required;
        });
        
        $("[name='password']").prop("required", function(i, required) {
            return !required;
        });        
    }
});