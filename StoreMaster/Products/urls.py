from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views

app_name = "Products"

urlpatterns = [
    path('products', views.index,name='index'),
    path('product_view/<int:product_id>ß',views.product_view,name="product_view"),
    path('product_edit_view/<int:product_id>',views.product_edit_view,name="product_edit_view"),
    path('<int:store_id>/add_product_view',views.add_product_view,name="add_product"),
    path("employee_view_product/<int:product_id>",views.employee_view_product,name="employee_view_product")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)