from django.urls import path

from . import views

app_name = "Accounts"

urlpatterns = [
    path('',views.index,name="home"),
    path('accounts', views.index,name='index'),
    path('login',views.login_user,name='login'),
    path('register_user',views.register_user,name='register_user'),
]