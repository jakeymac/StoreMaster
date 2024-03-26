

function load_data() {
    let csrftoken = $('meta[name="csrf-token"]').attr('value');
    console.log(csrftoken);
    fetch(`/api/product/${product_id}`, {
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
        var product = data.product;
        $("#stock-number-input").val(product.product_stock);

        if(product.product_image !== null) {
            var segments = product.product_image.split('/')
            if (segments.length >= 7) {
                var image_name = segments.slice(6).join('/');
                $("#product-image-link").text(image_name);
            } else {
                $("#product-image-link").text(product.product_image);
            }
            
            $("#product-image-link").attr('href',product.product_image);
        } else {
            $("#product-image-link").text("No image found");
        }

        $("#product-name-input").val(product.product_name);
        $("#product-description-input").val(product.product_description);
        $("#product-price-input").val(product.product_price);
        $("#product-location-input").val(product.product_location);
        $("#product-low-stock-quantity-input").val(product.low_stock_quantity);
    });
    
}       

function load_listeners() {
    let csrftoken = $('meta[name="csrf-token"]').attr('value');
    $("#save-button").on("click", function() {
        let new_product_data = new FormData();
        let image_input = $("#product-image-selection-input")[0].files[0];

        console.log("Image input");
        console.log(image_input);
        if (image_input !== null) {
            
            new_product_data.append('product_image', image_input);
            console.log(new_product_data);
            console.log("Ok step 1")
        } else {
            console.log("Step 2");
            if ($("#product-image-link").text() == "Removed Image") {
                console.log("Step 3");
                new_product_data.append('product_image', null);
            }
        }

        console.log(new_product_data);

        new_product_data.append('product_stock',$("#stock-number-input").val());
        new_product_data.append('product_name', $("#product-name-input").val());
        new_product_data.append('product_description', $("#product-description-input").val());
        new_product_data.append('product_price', $("#product-price-input").val());
        new_product_data.append('product_location', $("#product-location-input").val());
        new_product_data.append('low_stock_quantity', $("#product-low-stock-quantity-input").val());

       
        console.log(new_product_data);
        fetch(`/api/product/${product_id}`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: new_product_data

        })
        .then(response => {
            if (!response.ok) {
                Swal.fire({
                    icon:'error',
                    title:'Error Saving',
                    text:'There was an error saving product information',
                    timer: 3000,
                    timerProgressBar: false,
                    // customClass: {
                    //     popup: 'saved-successfully-alert'
                    // }
                });
                
            }
            return response.json();
        }).then (data => {
            console.log(data);
            Swal.fire({
                icon:'info',
                title:'Success',
                text:'Product information was saved successfully',
                timer: 3000,
                timerProgressBar: false,
                // customClass: {
                //     popup: 'saved-successfully-alert'
                // }
            });
            setTimeout(function() {
                window.location.href = `/employee_view_product/${product_id}`;
            }, 3000);
        });
        
        // let product_stock = $("#stock-number-input").val();
        // let product_name = $("#product-name-input").val();
        // let product_description = $("#product-description-input").val();
        // let product_price = $("#product-price-input").val();
        // let product_location = $("#product-location-input").val();
        // let product_low_stock_quantity = $("#product-low-stock-quantity-input").val();
    })

    $("#back-button").on("click", function() {
        window.location.href = `/employee_view_product/${product_id}`;
    })
}

$(document).ready(function() {
    
    load_data();
    load_listeners();
})