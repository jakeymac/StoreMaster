var products;
var orders;
var purchases;
var customers;
var employees;
var products_low_in_stock;

let csrftoken = $("input[name=csrfmiddlewaretoken]").val();

// Function to filter products based on search text by product name
function filterProducts(search_text) {
    var productsFound = false;
    $(".individual-product-div").each(function() {
        var productName = $(this).find('p').text().toLowerCase();
        if (productName.includes(search_text.toLowerCase())) {
            $(this).show(); // Show product if the search text matches
            productsFound = true;
        } else {
            $(this).hide(); // Hide product if the saerch text doesn't match
        }
    });
    if(!productsFound) {
        $("#no-products-text").show(); // Show "no products" message if no products were found in the search
    } else {
        $("#no-products-text").hide(); // Hide "no products" message if any products were found in the search

    }
}

// Function to filter orders based on search text by order ID and customer name
function filterOrders(search_text) {
    var ordersFound = false;
    $(".order-row").each(function() {
        var orderId = $(this).find(".order-id-cell").first().text();
        var orderCustomerName = $(this).find(".order-customer-name-cell").first().text();
        if(orderId.includes(search_text) || orderCustomerName.includes(search_text)) {
            ordersFound = true;
            $(this).show();  // Show order if the search text matches
        } else {
            $(this).hide(); // Hide order if the search text doesn't match
        }
    })

    if(!ordersFound) {
        $("#no-orders-text").show(); // Show "no orders" message if no orders were found in the search
        $("#order-info-table").hide(); // Hide the order results table headers
    } else {
        $("#no-orders-text").hide(); // Hide "no orders" message if any orders were found in the search
        $("#order-info-table").show(); // Show the order results table headers
    }
}

// Function to filter purchases based on search text by purchase ID and customer name
function filterPurchases(search_text) {
    var purchasesFound = false;
    $(".purchase-row").each(function() {
        var purchaseId = $(this).find(".purchase-id-cell").first().text();
        var purchaseCustomerName = $(this).find(".purchase-customer-name-cell").first().text();
        if(purchaseId.includes(search_text) || purchaseCustomerName.includes(search_text)) { //May adjust for employee search as well
            purchasesFound = true;
            $(this).show(); // Show purchase if the search text matches
        } else {
            $(this).hide(); // Hide purchase if the search text doesn't match
        } 
    })

    if (!purchasesFound) {
        $("#no-purchases-text").show(); // Show "no purchases" message if no purchases were found in the search
        $("#purchase-info-table").hide(); // Hide the purchase results table headers
    } else {
        $("#no-purchases-text").hide(); // Hide "no purchases" message if any purchases were found in the search
        $("#purchase-info-table").show(); // Show the purchase results table headers
    }
}

// Function to filter customers based on search text by name
function filterCustomers(search_text) {
    var customersFound = false;
    $(".individual-customer-div").each(function() {
        var customerName = $(this).find('p').text().toLowerCase();
        if(customerName.includes(search_text.toLowerCase())) {
            $(this).show(); // Show customer if the search text matches
            customersFound = true;
        } else {
            $(this).hide(); // Hide customer if the search text doesn't match
        }
    });

    if (!customersFound) {
        $("#no-customers-text").show(); // Show no customers message if no customers were found in the search
    } else {
        $("#no-customers-text").hide(); // Hide no customers message if any customers were found in the search
    }
}

// Function to filter employees based on search text by name
function filterEmployees(search_text) {
    var employeesFound = false;
    $(".individual-employee-div").each(function() {
        var employeeName = $(this).find('p').text().toLowerCase();
        if (employeeName.includes(search_text.toLowerCase())) {
            $(this).show(); // Show employee if the search text matches
            employeesFound = true; 
        } else {
            $(this).hide(); // Hide employee if the search text doesn't match
        }
    });

    if (!employeesFound) {
        $("#no-employees-text").show(); // Show no employees message if no employees were found in the search
    } else {
        $("#no-employees-text").hide(); // Hide no employees message if any employees were found in the search
    }
}



// Function to request and organize data from the server
function load_store_data() {
    
    fetch('/api/account/logged_in_account', {
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
        isAdmin = (data.account_info.account_type == "admin");
        $("#welcome-user-header").text(`Welcome, ${data.account_info.first_name}`);
        if (isAdmin) {
            $("#customer-search-section").show();
            $("#employee-search-section").show();
            load_admin_only_data();
        }
    })
    fetch(`api/store/${store_id}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    })
    .then(response=> {
        if (!response.ok) {
            throw new Error('network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        var store = data.store;
        $("#store-name-header").text(store.store_name);
    });

    // Retrieve all the products in the store
    fetch(`/api/product/store/${store_id}/true`, {
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
    }).then(data => {
        products = data.products;
        if (products.length == 0) {
            $("#no-products-text").show();
        } 
        products.forEach(function(product) {    
            var new_product_div = `<div class="individual-product-div"> 
                                        <p class="product-name-p" >${product.product_name}</p> 
                                        <button class="view-product-button" product_id="${product.product_id}">View</button>
                                   </div>`;


            $("#product-results-div").append(new_product_div);
        })

        products_low_in_stock = data.products_low_in_stock;
        if (products_low_in_stock.length == 0) {
            $("#no-low-stock-text").show();
        }
        products_low_in_stock.forEach(function(product) {
            // Style each product differently for items that are out of stock, or just low in stock
            if (product.product_stock == 0) {
                var stock_class = "out-of-stock-item";
            } else {
                var stock_class = "low-stock-item"
            }
            // Generate html for each product and add it to the list of products that are low in stock
            var new_product_html = `<div class="individual-product-div">
                                        <p class="product-name-p ${stock_class}"> ${product.product_name}</p>
                                        <button class="view-product-button" product_id="${product.product_id}">View</button>
                                    </div>`
            $("#low-stock-items").append(new_product_html);
        });
    });
    
    // Retreive all orders from the store
    fetch(`/api/order/store/${store_id}`, {
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
        orders = data.orders;
        console.log(orders);
        if (orders.length == 0) {
            $("#no-orders-text").show();
            $("#order-info-table").hide();
        }
        var new_order_div_html = "";
        orders.forEach(function(order) {
            // Reformat the order date for displaying
            var order_date = new Date(order.order_date);
            var month = String(order_date.getMonth() + 1).padStart(2, '0'); 
            var day = String(order_date.getDate()).padStart(2, '0');
            var year = order_date.getFullYear();
            var formattedDate = `${month}-${day}-${year}`;
            

            // Generate html for each order and add it to the order results table
            new_order_div_html += `<tr class="order-row">
                                        <td class="order-id-cell">${order.order_id}</td>
                                        <td class="order-date-cell">${formattedDate}</td>
                                        <td class="order-customer-name-cell">${order.customer_id.first_name} ${order.customer_id.last_name}</td>
                                        <td><button class="view-order-button" order_id="${order.order_id}" customer_id="${order.customer_id.user.id}">View</button> </td>
                                    </tr>`
        });
    
        $("#order-info-table").append(new_order_div_html);
    })

    // Retreive all purchases from store
    fetch(`/api/purchase/store/${store_id}`, {
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
        purchases = data.purchases;
        console.log(purchases);
        if (purchases.length == 0) {
            $("#no-purchases-text").show();
            $("#purchase-info-table").hide();
        }

        // Empty html string to add to
        var new_purchase_div_html = "";
        
        purchases.forEach(function(purchase) {
            // Reformat the purchase date for displaying
            var purchase_date = new Date(purchase.purchase_date);
            var month = String(purchase_date.getMonth() + 1).padStart(2,'0');
            var day = String(purchase_date.getDate()).padStart(2,'0');
            var year = purchase_date.getFullYear();
            var formattedDate = `${month}-${day}-${year}`;
            var customer_name = "";
            if (purchase.customer_id !== null) {
                customer_name = purchase.customer_id.first_name + " " + purchase.customer_id.last_name;
            } else if (purchase.first_name !== null) {
                customer_name = purchase.first_name;
                if (purchase.last_name !== null)  {
                    customer_name += " " + purchase.last_name;
                }
            } else {
                customer_name = "No name found";
            }

            // Generate html for each purchase and add it to the purchase results table
            new_purchase_div_html += `<tr class="purchase-row">
                                        <td class="purchase-id-cell">${purchase.purchase_id}</td>
                                        <td class="purchase-date-cell">${formattedDate}</td>
                                        <td class="purchase-customer-name-cell">${customer_name}</td>
                                        <td><button class="view-purchase-button" purchase_id="${purchase.purchase_id}" customer_id="${purchase.customer_id.user.id}">View</button></td>
                                      </tr>`
        });
        $("#purchase-info-table").append(new_purchase_div_html); 
    })
}

function load_admin_only_data() {
    // Retrieve all customers in store
    fetch(`/api/account/customer/${store_id}`, {
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
        var customers = data.customers;
        if(customers.length == 0) {
            $("#no-customers-text").show();
        }
        customers.forEach(function(customer) {
            console.log(customer);
            // Generate html for each customer and add it to the customer search results section
            var new_customer_html = `<div class="individual-customer-div">
                                        <p class="customer-name-p">${customer.first_name} ${customer.last_name}</p>
                                        <button class="view-customer-button" customer_id="${customer.user.id}">View</button>
                                    </div>`;

            $("#customer-results-div").append(new_customer_html);
        });
    })

    // Retreive all employees in store
    fetch(`/api/account/employee/${store_id}`, {
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
        var employees = data.employees;
        if (employees.length == 0) {
            $("#no-employees-text").show();
        }
        employees.forEach(function(employee) {
            console.log(employee);
            // Generate html for each employee and add it to the employee search results section
            var new_employee_html = `<div class="individual-employee-div">
                                        <p class="employee-name-p">${employee.first_name} ${employee.last_name}</p>
                                        <button class="view-employee-button" employee_id="${employee.user.id}">View</button>
                                     </div>`

            $("#employee-results-div").append(new_employee_html);
        });
    })
}


function load_listeners() {
    // Event listener for the product search bar
    $("#product-search-bar").on('input', function() {
        var search_text = $(this).val().trim();
        filterProducts(search_text);
    });
    
    // Event listener for the order search bar
    $("#order-search-bar").on("input", function() {
        var search_text = $(this).val().trim();
        filterOrders(search_text);
    });

    // Event listener for the purchase search bar
    $("#purchase-search-bar").on("input", function() {
        var search_text = $(this).val().trim();
        filterPurchases(search_text);
    });

    // Event listener for the customer search bar
    $("#customer-search-bar").on("input", function() {
        var search_text = $(this).val().trim();
        filterCustomers(search_text);
    });

    // Event listener for the employee search bar
    $("#employee-search-bar").on("input", function() {
        var search_text = $(this).val().trim();
        filterEmployees(search_text);
    });

    // Event listener for view product buttons
    $(document).on("click", ".view-product-button", function() {
        var product_id = $(this).attr("product_id");
        $("#product-id-input").val(product_id);
        $("#open-product-form").submit();
    });

    // Event listener for view order buttons
    $(document).on("click", ".view-order-button", function() {
        var order_id = $(this).attr("order_id");
        var customer_id = $(this).attr("customer_id");
        $("#order-id-input").val(order_id);
        $("#order-customer-id-input").val(customer_id);
        $("#open-order-form").submit();
    });

    // Event listener for view purchase buttons
    $(document).on("click", ".view-purchase-button", function() {
        var purchase_id = $(this).attr("purchase_id");
        var customer_id = $(this).attr("customer_id");
        $("#purchase-id-input").val(purchase_id);
        $("#purchase-customer-id-input").val(customer_id);
        $("#open-purchase-form").submit();
    });

    // Event listener for view customer buttons
    $(document).on("click", ".view-customer-button", function() {
        var customer_id = $(this).attr("customer_id");
        $("#customer-id-input").val(customer_id);
        $("#open-customer-form").submit();
    });

    // Event listener for view employee buttons
    $(document).on("click", ".view-employee-button", function() {
        var employee_id = $(this).attr("employee_id");
        // Open the view employee page with the chosen employee ID
        window.location.href = `/view_employee/${employee_id}`;
    });

    //Event listeners for manager/admin menu buttons
    $(document).on("click", "#view-all-shipments-button", function() {
        window.location.href = `/view_all_shipments/${store_id}`;
    });

    $(document).on("click", "#add-product-button", function() {
        window.location.href = `/add_product/${store_id}`;
    });

    $(document).on("click", "#new-purchase-button", function() {
        window.location.href = `/new_purchase/${store_id}`;
    });

    $(document).on("click", "#add-new-manager-button", function() {
        window.location.href = `/register_employee`;
    });
    
    $(document).on("click", "#return-to-admin-portal-button", function() {
        window.location.href = `/admin_manage_stores`;
    });

    $(document).on("click", "#log-out-button", function() {
        window.location.href = `/logout_employee`;
    });
}

$(document).ready(function() {
    load_store_data();
    load_listeners();
});