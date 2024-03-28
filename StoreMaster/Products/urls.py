from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views
from . import endpoints

app_name = "Products"

urlpatterns = [
    path('products', views.index,name='index'),
    path('view_product',views.product_view,name="view_product"),
    path('edit_product',views.edit_product_view,name='edit_product'),
    path("employee_view_product/<int:product_id>",views.employee_view_product,name="employee_view_product"),
    path("delete_product/<int:product_id>",views.delete_product,name="delete_product"),
    path("add_product/<int:store_id>", views.add_product_view, name="add_product"),
    
    path("api/product/product_in_order", endpoints.product_in_order_endpoint),
    path("api/product/product_in_order/<int:id>", endpoints.product_in_order_endpoint),
    path("api/product/product_history/<int:id>", endpoints.product_history_endpoint),
    path('api/product/search/<int:store_id>', endpoints.product_search_endpoint),
    path('api/product/search/<int:store_id>/<str:search_text>', endpoints.product_search_endpoint),
    path('api/product/search/<int:store_id>/<str:search_text>/<str:sort>', endpoints.product_search_endpoint),
    path("api/product",endpoints.product_endpoint),
    path("api/product/<int:id>", endpoints.product_endpoint),
    path("api/product/<str:id_type>/<int:id>",endpoints.product_endpoint),
    path("api/product/<str:is_active>", endpoints.product_endpoint),
    path("api/product/<str:id_type>/<int:id>/<str:is_active>",endpoints.product_endpoint),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)