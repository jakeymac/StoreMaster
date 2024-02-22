// {% if no_results %} 
//                     <p>{{ no_results }}</p>                
//                 {% else %}
//                     {% for result in results %} 
//                         <div class="store-entry">
//                             <div class="store-info">
//                                 <p class="store-name">{{result.store_name}}</p>
//                                 <p class="store-address">{{result.address}} {{result.line_two}} {{result.city}}</p>
//                             </div>
//                             <a href="{% url 'Stores:store_home' result.store_id %}"><button class="open-store-button">Open Store</button></a>
//                         </div>
//                     {% endfor %}
//                 {% endif %}


var get_store_search_results = function() {
    var searchTerm = $("#home-store-search-bar").val();

    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    
    var data = {
        search_term: searchTerm,
        csrfmiddlewaretoken: csrftoken
    };

    fetch('search_for_stores', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('network response was not ok');
        } 
        return response.json();
    })
    .then(data => {
        //Parse from string to object
        data = JSON.parse(data);
        console.log("Re-parsed: ", data);
        console.log("Problems");
        console.log("Length: ", data.length);
        let resultsDiv = $("#search-results-div");
        resultsDiv.show();
        
        if (data.length > 0) {
            console.log("Yep");
            var resultsHTML = "";
            data.forEach(function(store) {
                console.log(store);
                store_html = `<div class="store-entry">
                                <div class="store-info">
                                    <p class="store-name">${store.fields.store_name}</p>
                                    <p class="store-address">"${store.fields.address} ${store.fields.line_two} ${store.fields.city}"</p>
                                </div>
                                <button id="open-store-result-${store.pk}" class="open-store-button">Open Store</button>
                            </div>`

                resultsHTML += store_html;
                
                console.log(store.fields.store_name);
            });
        } else {
            resultsHTML = "<p>No results found</p>";
        }

        

        resultsDiv.html(resultsHTML);
        //console.log(resultsHTML);
        console.log("Success");
        resultsDiv.on('click', '.open-store-button', function() {
            var storeId = this.id.split("-")[3];
            console.log(storeId);
            var url = "store_home/O ".replace('O',storeId);
            window.location.href=url; 
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

$(document).ready(function() {
    $("#search-results-div").hide();
    $("#home-store-search-button").click(function () {
        get_store_search_results();
    });
});