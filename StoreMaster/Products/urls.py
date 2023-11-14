from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from . import views

app_name = "Products"

urlpatterns = [
    path('products', views.index,name='index'),
    path('<int:store_id>/product_view/<int:product_id>',views.product_view,name="product_view"),
    path('<int:store_id>/product_edit_view/<int:product_id>',views.product_edit_view,name="product_edit_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)