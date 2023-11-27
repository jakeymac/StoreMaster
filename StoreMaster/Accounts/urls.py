from django.urls import path

from . import views

app_name = "Accounts"

urlpatterns = [
    path('',views.index,name="home"),
    path('accounts', views.index,name='index'),
    path('login',views.login_user,name='login'),
    path('register_user',views.register_user,name='register_user'),
    path('select_user',views.select_user_view,name='select_user'),
    path('edit_user/<int:user_id>',views.edit_user_view,name='edit_user'),
    path('view_user/<int:user_id>',views.view_user,name="view_user")
]