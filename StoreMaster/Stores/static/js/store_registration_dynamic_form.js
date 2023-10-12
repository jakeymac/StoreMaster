$(document).ready(function () {
    var form = $('#store_registration_form')
    var addManagerFormButton = $('#add_new_manager_form_button')
    addManagerFormButton.click(function (e) {
        e.preventDefault();
        var newForm = `<div>
                        <input type="text" name="manager_name" placeholder="Manager Name"> <br>
                        <input type="text" name="manager_last_name" placeholder="Manager Last Name"> <br>
                        <input type="text" name="manager_address" placeholder="Manager Address"> <br>
                        <input type="text" name="manager_line_two" placeholder="Manager Address Line 2"> <br>
                        <input type="text" name="manager_city" placeholder="Manager City"> <br>
                        <input type" text" name="manager_state" placeholder="Manager State"> <br>
                        <input type="text" name="manager_zip" placeholder="Manager ZIP Code"> <br>
                        <input type="text" name="manager_username" placeholder="Manager Username"> <br>
                        <input type="password" name="manager_password" placeholder="Manager Password"> <br>
                        <input type="text" name="manager_other_info" placeholder="Other Manager Info"> <br>
                        <input type="date" name="manager_birthday" placeholder="Manager Birthday"> <br>
                      </div>`
        form.append(newForm);

        addManagerFormButton.hide();
        
    });
});