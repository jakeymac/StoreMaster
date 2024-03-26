function load_data() {
    let csrftoken = $('meta[name="csrf-token"]').attr('content');
    fetch(`/api/store/${store_id}`, {
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
        $("#store-name-header").text(data.store.store_name);
    });

    fetch(`/api/product/search/${store_id}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('network response was not ok');
        }
        return response.json();
    })
    .then(data => { 
        console.log(data);
        var products = data.products;
        display_products(products);
    });

}


function display_products(products) {
    $(".row").children(".product").remove();
    if (products.length == 0) {
        $("#no-products-p").show();
    } else {
        var product_count = 0;
        var product_html = '<div class="row">';
        products.forEach(function(product) {
            if (product_count % 4 === 0 && product_count !== 0) {
                product_html += '</div><div class="row">';
            }
    
            product_html += '<div class="product">';
            if (product.product_image) {
                product_html += `<img src="${product.product_image}" alt="${product.product_name}">`;
            }
            product_html += `<a href="/product_view/${product.product_id}" class="product-link"><h2>${product.product_name}</h2></a>
                             <p>$${product.product_price}</p>
                             </div>`;
            
            product_count++;
            
            
        });
    
        var remainder = product_count % 4;
        if (remainder !== 0) {
            for (var i = 0; i < 4 - remainder; i++) {
                product_html += '<div class="product empty-product"></div>';
            }
        }
    
        product_html += '</div>';
        $("#search-results").append(product_html);
    }
}
   

function load_listeners() {
    $("#search-button").on("click", function() {
        console.log("Trying");
        let csrftoken = $('meta[name="csrf-token"]').attr('content');
        var search_text = $("#search-bar").val();
        if ($("#sort-selector").val()) {
            var sort = $("#sort-selector").val();
            var url = `/api/product/search/${store_id}/${search_text}/${sort}`;
        } else {
            var url = `/api/product/search/${store_id}/${search_text}`;
        }
        
        fetch(url, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error('network response was not ok');
            }
            return response.json();
        })
        .then(data => { 
            console.log(data);
            var products = data.products;
            display_products(products);
        });
    })
}

$(document).ready(function() {
    load_data();
    load_listeners();
})