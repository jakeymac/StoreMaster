from django.urls import path

from . import views
from . import endpoints

app_name = "Orders"

urlpatterns = [
    path('orders', views.index,name='index'),
    path('view_customer_orders/<int:user_id>',views.view_customer_orders,name="view_customer_orders"),
    path('view_order/<int:order_id>',views.view_order,name="view_order"),

    path('api/order', endpoints.order_endpoint),
    path('api/order/<int:id>', endpoints.order_endpoint),
    path('api/order/<str:id_type>/<int:id>',endpoints.order_endpoint)
]