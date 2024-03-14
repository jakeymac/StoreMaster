function load_product_data() {
    console.log("Loading product data");
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(store_id, {
        method: "POST",
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
        var order_averages = data.order_averages;
        var purchase_averages = data.purchase_averages;
        var overall_averages = data.overall_averages;

        $("#product-name-header").text(product.product_name);
        $("#product-price-p").text(`$${product.product_price}`);
        $("#product-description-p").text(product.product_description);
        $("#product-in-stock-p").text(product.product_stock);
        $("#product-location-p").text(product.product_location);

        $("#table-info-row").append(`<td id="order-averages-daily-td">${order_averages.daily}</td>
                                     <td id="order-averages-weekly-td">${order_averages.weekly}</td>
                                     <td id="order-averages-monthly-td">${order_averages.monthly}</td>
                                     <td id="purchase-averages-daily-td">${purchase_averages.daily}</td>
                                     <td id="purchase-averages-weekly-td">${purchase_averages.weekly}</td>
                                     <td id="purchase-averages-monthly-td">${purchase_averages.monthly}</td>
                                     <td id="overall-averages-daily-td">${overall_averages.daily}</td>
                                     <td id="overall-averages-weekly-td">${overall_averages.weekly}</td>
                                     <td id="overall-averages-monthly-td">${overall_averages.monthly}</td>`);

        
        
    })

}

function load_listeners() {
    console.log("Loading product data listeners");
}

$(document).ready(function() {
    load_product_data();
    load_listeners();
});