from django.urls import path

from . import views

app_name = "Products"

urlpatterns = [
    path('products', views.index,name='index'),
]