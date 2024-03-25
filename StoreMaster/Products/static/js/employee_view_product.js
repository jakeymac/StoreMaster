var product_history;
var product_data;
let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
function load_product_data() {
    

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
        product_data = data.product;
        var product = data.product;
    
        $("#product-name-header").text(product.product_name);
        $("#product-price-p").text(`$${product.product_price}`);
        $("#product-description-p").text(product.product_description);
        $("#product-in-stock-p").text(product.product_stock);
        $("#product-location-p").text(product.product_location);

        if (product.product_image) {
            $("#no-image-div").hide();
            $("#product-image").attr("src", product.product_image);
            $("#product-image").show();
        } else {
            $("#no-image-div").show();
        }
    })

    fetch(`/api/product/product_history/${product_id}`,{
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
        console.log("product history api data: ", data);
        var product = data.product;
        product_history = data.product_history_data;

        var daily_order_average = product_history.orders_daily_average;
        var weekly_order_average = product_history.orders_weekly_average;
        var monthly_order_average = product_history.orders_monthly_average;

        var daily_purchase_average = product_history.purchases_daily_average;
        var weekly_purchase_average = product_history.purchases_weekly_average;
        var monthly_purchase_average = product_history.purchases_monthly_average;

        var daily_overall_average = product_history.overall_daily_average;
        var weekly_overall_average = product_history.overall_weekly_average;
        var monthly_overall_average = product_history.overall_monthly_average;

        $("#orders-info-row").append(`<td id="order-averages-daily-td">${daily_order_average}</td>
                                      <td id="order-averages-weekly-td">${weekly_order_average}</td>
                                      <td id="order-averages-monthly-td">${monthly_order_average}</td>`);

        $("#purchases-info-row").append(`<td id="purchase-averages-daily-td">${daily_purchase_average}</td>
                                         <td id="purchase-averages-weekly-td">${weekly_purchase_average}</td>
                                         <td id="purchase-averages-monthly-td">${monthly_purchase_average}</td>`);
                                         
        $("#overall-info-row").append(`<td id="overall-averages-daily-td">${daily_overall_average}</td>
                                       <td id="overall-averages-weekly-td">${weekly_overall_average}</td>
                                       <td id="overall-averages-monthly-td">${monthly_overall_average}</td>`);                                  
    }) 
}

function load_listeners() {
    console.log("Loading product data listeners");
    $("#view-graph-button").on("click", function() {
        load_graph();
    });

    $("#edit-product-button").on("click", function() {
        window.location.href = `/product_edit_view/${product_data.product_id}`;
    });

    $("#delete-product-button").on("click", function() {
        Swal.fire({
            title: 'Are you sure?',
            text: "Are you sure you want to delete this product? You won't be able to undo this",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            customClass: {
                popup: 'delete-alert'
            }
        }).then((result) => {
            console.log(result);
            if (result.isConfirmed) {
                // Send a DELETE request to API
                console.log()
                fetch(`/api/product/${product_data.product_id}`, {
                    method: 'DELETE',
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        Swal.fire({
                            title: 'Error',
                            text: 'There was an error deleting this product',
                            icon: 'error',
                            timer:3000,
                            timerProgressBar: false,
                            customClass: {
                                popup: 'delete-confirmation-alert'
                            }
                        });
                    } else {
                        Swal.fire({
                            title: 'Deleted',
                            text: 'Successfully deleted this product',
                            icon: 'success',
                            timer:3000,
                            timerProgressBar: false,
                            customClass: {
                                popup: 'delete-confirmation-alert'
                            }
                        });
                        window.location.href = `/manage_store/${product.store.store_id}`;             
                    }

                })
                Swal.fire({
                    title: 'Deleted',
                    text: 'Successfully deleted',
                    icon: 'success',
                    timer:3000,
                    timerProgressBar: false,
                    customClass: {
                        popup: 'delete-confirmation-alert'
                    }
                });
            }
        })
    });

    $("#return-to-portal-button").on("click", function() {
        window.location.href = `/manage_store/${product_data.store.store_id}`;

    });
    
}

function load_graph() {
    

    if ($("#source-selector").val() != "" && $("#time-selector").val() != "") {
        var source = $("#source-selector").val();
        var time  = $("#time-selector").val();
        // console.log("Success");
        // console.log(graph_data);

        var selected_combo = product_history[`${source}_${time}_total_results`]
        var source_text = source.charAt(0).toUpperCase() + source.slice(1).toLowerCase();
        var time_text = time.charAt(0).toUpperCase() + time.slice(1).toLowerCase();


        var times = Object.keys(selected_combo);
        var values = Object.values(selected_combo);

        var x_title;
        if (time == "daily") {
            x_title = "Day";
        } else if (time == "weekly") {
            x_title = "Week";
        } else {
            x_title = "Month";
        }

        if (source == "overall") {
            source_text = "Orders/Purchases"
            
        } 

        var data  = [
            {
                x: times,
                y: values,
                mode: 'lines+markers',
                type: 'scatter',
                name: `${time} ${source} `
            }
        ];
        var layout = {title: `${time_text} ${source_text} `,
                      xaxis: {
                        title: x_title
                      },
                      yaxis: {
                        title: `${source_text}`
                      }
        };
        Plotly.newPlot('graph-div', data, layout);
    }
}



$(document).ready(function() {
    load_product_data();
    load_listeners();
    // Load an empty graph
    Plotly.newPlot("graph-div", [],{});
});