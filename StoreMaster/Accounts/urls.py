from django.urls import path

from . import views

app_name = "Accounts"

urlpatterns = [
    path('',views.index,name="home"),
    path('accounts', views.index,name='index'),
    path('login_customer',views.login_customer,name='login_customer'),
    path('login_employee',views.login_employee,name='login_employee'),
    path('register_customer',views.register_customer,name='register_customer'),
    path('register_employee',views.register_employee,name='register_employee'),
    path('select_user',views.select_user_view,name='select_user'),
    path('edit_user/<int:user_id>',views.edit_user_view,name='edit_user'),
    path('view_customer/<int:user_id>',views.view_customer,name='view_customer'),
    path('edit_customer/<int:user_id>',views.edit_customer,name='edit_customer'),
    path('logout_employee',views.logout_employee,name='logout_employee'),
    path('logout_customer',views.logout_customer,name='logout_customer'),
    
]