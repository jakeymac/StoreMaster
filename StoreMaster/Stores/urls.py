from django.urls import path

from . import views

app_name = "Stores"

urlpatterns = [
    path('stores', views.index,name='index'),
    path('search_for_store', views.search_for_store, name='search_for_store'),
    path('register_store',views.register_store_page_1,name='register_store_page_1'),
    path('register_store_manager',views.register_store_page_2,name='register_store_page_2'),
    path('manage_store/<int:store_id>',views.manage_store,name='manage_store'),
    path("admin_manage_stores",views.admin_manage_stores,name='admin_manage_stores'),
    path('confirm_store_registration',views.confirm_store_registration,name="confirm_store_registration"),
    path('manage_store_redirect_from_home', views.manage_store_redirect_from_home,name='manage_store_home_page_redirect'),
    path('product_search',views.product_search, name='product_search'),
    path('store_home/<int:store_id>',views.store_home,name="store_home"),
    path('view_customer_cart/<int:user_id>',views.view_customer_cart,name="view_customer_cart"),
    path('edit_customer_cart/<int:user_id>',views.edit_customer_cart,name="edit_customer_cart"),
    path('new_purchase/<int:store_id>',views.new_purchase,name="new_purchase"),
    path('add_product_to_purchase/<int:store_id>/<int:product_id>/<int:quantity>',views.add_product_to_purchase,name="add_product_to_purchase"),
    path('employee_view_purchase/<int:purchase_id>',views.employee_view_purchase,name="employee_view_purchase"),
    path('view_shipment/<int:shipment_id>',views.view_shipment,name='view_shipment'),\
    path('view_all_shipments/<int:store_id>',views.view_all_shipments,name='view_all_shipments'),
    path('employee_view_customer/<int:customer_id>',views.employee_view_customer,name='employee_view_customer'),
    path('employee_view_employee/<int:employee_id>',views.employee_view_employee,name='employee_view_employee'),
    path('employee_view_product/<int:product_id>',views.employee_view_product,name='employee_view_product'),

]   