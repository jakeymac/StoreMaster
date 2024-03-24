from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views
from . import endpoints

app_name = "Products"

urlpatterns = [
    path('products', views.index,name='index'),
    path('product_view/<int:product_id>ß',views.product_view,name="product_view"),
    path('product_edit_view/<int:product_id>',views.product_edit_view,name="product_edit_view"),
    path("employee_view_product/<int:product_id>",views.employee_view_product,name="employee_view_product"),
    path("delete_product/<int:product_id>",views.delete_product,name="delete_product"),
    path("add_product/<int:store_id>", views.add_product_view, name="add_product"),
    
    path("api/product/product_in_order", endpoints.product_in_order_endpoint),
    path("api/product/product_in_order/<int:id>", endpoints.product_in_order_endpoint),
    path("api/product",endpoints.product_endpoint),
    path("api/product/<int:id>", endpoints.product_endpoint),
    path("api/product/<str:id_type>/<int:id>",endpoints.product_endpoint),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)