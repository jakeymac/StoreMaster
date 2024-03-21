let graph_data;
var product_data;
function load_product_data() {
    console.log("Loading product data");
    let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
    fetch(window.location.href, {
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

        graph_data = data.graph_data;
        product_data = product;

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

        $("#orders-info-row").append(`<td id="order-averages-daily-td">${order_averages.daily}</td>
                                      <td id="order-averages-weekly-td">${order_averages.weekly}</td>
                                      <td id="order-averages-monthly-td">${order_averages.monthly}</td>`);

        $("#purchases-info-row").append(` <td id="purchase-averages-daily-td">${purchase_averages.daily}</td>
                                          <td id="purchase-averages-weekly-td">${purchase_averages.weekly}</td>
                                          <td id="purchase-averages-monthly-td">${purchase_averages.monthly}</td>`);
                                          
        $("#overall-info-row").append(`<td id="overall-averages-daily-td">${overall_averages.daily}</td>
                                       <td id="overall-averages-weekly-td">${overall_averages.weekly}</td>
                                       <td id="overall-averages-monthly-td">${overall_averages.monthly}</td>`);                            
    })
}

function load_listeners() {
    console.log("Loading product data listeners");
    $("#view-graph-button").on("click", function() {
        load_graph();
    });

    $("#edit-product-button").on("click", function() {
        console.log("Edit product button");
        window.location.href = `/product_edit_view/${product_data.product_id}`;
    });

    $("#delete-product-button").on("click", function() {
        console.log("Delete product button");
        window.location.href = `/delete_product/${product_data.product_id}`;
    });

    $("#return-to-portal-button").on("click", function() {
        console.log("Return to portal");
        window.location.href = `/manage_store/${product_data.store_id}`;

    });
    
}

function load_graph() {
    

    if ($("#source-selector").val() != "" && $("#time-selector").val() != "") {
        var source = $("#source-selector").val();
        var time  = $("#time-selector").val();
        console.log("Success");
        console.log(graph_data);

        var selected_combo = graph_data[`${source}_${time}_total_results`]
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