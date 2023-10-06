from django.urls import path

from . import views

app_name = "Purchases"

urlpatterns = [
    path('purchases', views.index,name='index'),
]