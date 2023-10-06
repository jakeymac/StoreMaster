from django.urls import path

from . import views

app_name = "Shipments"

urlpatterns = [
    path('shipments', views.index,name='index'),
]