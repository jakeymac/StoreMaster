from django.urls import path

from . import views

app_name = "Stores"

urlpatterns = [
    path('stores', views.index,name='index'),
    path('register_store',views.register_store_page_1,name='register_store_page_1'),
    path('register_store_manager',views.register_store_page_2,name='register_store_page_2'),
    path('manage_store/<str:store_name>',views.manage_store,name='manage_store'),
    path('confirm_store_registration',views.confirm_store_registration,name="confirm_store_registration"),
    path('manage_store_redirect_from_home', views.manage_store_redirect_from_home,name='manage_store_home_page_redirect'),
    path('product_search',views.product_search, name='product_search'),
    
]