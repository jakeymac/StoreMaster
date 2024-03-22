from django.urls import path

from . import views
from . import endpoints
from .views import ResetPasswordView
from django.contrib.auth import views as auth_views
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
    path('view_user/<int:user_id>',views.view_user,name='view_user'),
    path('employee_edit_customer/<int:customer_id>',views.employee_edit_customer,name='employee_edit_customer'),
    path('employee_view_customer/<int:customer_id>',views.employee_view_customer,name='employee_view_customer'),
    path('employee_view_customer/<int:customer_id>/<str:original_page>',views.employee_view_customer,name='employee_view_customer'),
    path('view_employee/<int:employee_id>/',views.view_employee,name='view_employee'),
    path('view_employee/<int:employee_id>/<str:original_page>',views.view_employee,name='view_employee'),
    path('edit_employee/<int:employee_id>', views.edit_employee_view, name='edit_employee'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/',views.login_employee,name='login'), # could be updated

    path('api/edit_employee', endpoints.edit_employee_endpoint, name='edit_employee_endpoint')
 ] 