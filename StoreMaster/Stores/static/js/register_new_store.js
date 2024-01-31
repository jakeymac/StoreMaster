$(document).ready(function() {
    $("#message-space").hide();
    $("#store_registration_form_1").submit(function(event) {
        event.preventDefault();
        
        var storeName = $("#store-name-entry").val();
        var storeAddress = $("#store-address-entry").val();
        var storeLineTwo = $("#store-line-two-entry").val();
        var storeCity = $("#store-city-entry").val();
        var storeState = $("#store-state-entry").val();
        var storeZip = $("#store-zip-entry").val();

        console.log("Store Name: ", storeName);
        console.log("zip:", storeZip);
        
        var complete = true;
        if (storeName.trim() === "") {
            complete = false;
        }   
        
        if (storeAddress.trim() === "") {
            complete = false;
        }
        
        if (storeCity.trim() === "") {
            complete = false;
        }

        if (storeState.trim() === "") {
            complete = false;
        }

        if(storeZip.trim() === "") {
            complete = false;
        }
        
        if (complete) {
            console.log("You're good");
        }

        requestData = {
            "step": 1,
            "name": storeName,
            "address": storeAddress,
            "line_two": storeLineTwo,
            "city": storeCity,
            "state": storeState,
            "zip": storeZip
        };

    })
});