from django.urls import path

from . import views
from . import endpoints

app_name = "Purchases"

urlpatterns = [
    path('purchases', views.index,name='index'),

    path('api/purchase',endpoints.purchase_endpoint),
    path('api/purchase/<int:id>',endpoints.purchase_endpoint),
    path('api/purchase/<id_type>/<int:id>',endpoints.purchase_endpoint)
]