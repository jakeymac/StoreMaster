let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
var store_id;
var customer_id;
function load_data() {
    fetch(`/api/order/${order_id}`, {
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
        var order = data.order;
        store_id = order.store.store_id;
        customer_id = order.customer_id.user.id;
        $("#order-id-p").text("Order ID: " + order.order_id);
        $("#order-date-p").text("Order Date: " + order.order_date);
        $("#customer-name-p").html(`Customer name: <span class="hoverable-link">${order.customer_id.first_name} ${order.customer_id.last_name}</span>`);
        $("#order-total-p").text("Order total: $" + order.order_total);
    });

    fetch(`/api/product/product_in_order/${order_id}`, {
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
        var products = data.products_in_order;

        var html_string = "";

        products.forEach(function(product_in_order) {
            var product_id = product_in_order.product.product_id;
            var product_name = product_in_order.product.product_name;
            var product_price = product_in_order.product.product_price;
            var quantity = product_in_order.quantity;

            html_string += `<tr>
                                <td id="product-id-cell">${product_id}</td>
                                <td><span class="hoverable-link">${product_name}</span></td>
                                <td>$${product_price}</td>
                                <td>${quantity}</td>
                            </tr>`;
        });

        $("#order-table").append(html_string);
    })
}

function load_listeners() {
 // Add functioanlity to have customer name and product names be 
 // clickable to open those pages ot the customer or pdocut details pages
    $("#back-button").on("click", function() {
        $("#store-id-input").val(store_id);
        $("#return-to-management-portal-form").submit();
        // window.location.href=`/manage_store/${store_id}`;
    })

    $("#order-information-div").on("click", ".hoverable-link", function() {
        console.log(customer_id);
        window.location.href=`/employee_view_customer/${customer_id}`;
    })
    $("#order-table").on("click", ".hoverable-link", function() {
        var product_id = $(this).closest("tr").find("#product-id-cell").text();
        window.location.href=`/employee_view_product/${product_id}`;
    })
}

$(document).ready(function() {
    load_data();
    load_listeners();
});