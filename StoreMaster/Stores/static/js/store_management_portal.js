var products;
var orders;
var purchases;
var customers;
var employees;
var products_low_in_stock;


function filterProducts(search_text) {
    var productsFound = false;
    $(".individual-product-div").each(function() {
        var productName = $(this).find('p').text().toLowerCase();
        if (productName.includes(search_text.toLowerCase())) {
            $(this).show();
            productsFound = true;
        } else {
            $(this).hide();
        }
    });
    if(!productsFound) {
        $("#no-products-text").show();
    } else {
        $("#no-products-text").hide();

    }
}

function load_store_data() {
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();    
    fetch(store_id, { //Send the store_id that is passed within the html through context
        method:'POST',
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
        products = data["products"];
        if (products.length == 0) {
            $("#no-products-text").show();
        }
        products.forEach(function(product) {
            var new_product_div = `<div class="individual-product-div"> 
                                        <p class="product-name-p" >${product.product_name}</p> 
                                        <button class="view-product-button" product_id="${product.product_id}">View</button>
                                    </div>`;

            $("#product-results-div").append(new_product_div);
        });
        
        orders = data["orders"];
        orders.forEach(function(order) {
            var new_order_div = `<div class="individual-order-div">
                                    <table class="order-info-table"> 
                                        <tr>
                                            <th>Order ID</th>
                                            <th>Date</th>
                                        </tr>
                                        <tr>
                                            <td>${order.order_id}</td>
                                            <td>${order.order_date}</td>
                                        </tr>
                                    </table>
                                    <button class="view-order-button" order_id="${order.order_id}">View</button>
                                </div>`;

            $("#order-results-div").append(new_order_div);

            
        });
            
            
        

        orders = data["orders"];
        purchases = data["purchases"];
        customers = data["customers"];
        employees = data["employees"];
        products_low_in_stock = data["products_low_in_stock"];
    })
}

function load_listeners() {
    $("#product-search-bar").on('input', function() {
        var search_text = $(this).val().trim();
        filterProducts(search_text);
    });

    $(document).on("click", ".view-product-button", function () {
        var product_id = $(this).attr("product_id");
        window.location.href = `/employee_view_product/${product_id}`;
    });
}

function load_page() {
    console.log("hi");
}

$(document).ready(function() {
    console.log("Loaded up the script");
    load_store_data();

    load_listeners();
});