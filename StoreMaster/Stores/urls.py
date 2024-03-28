from django.urls import path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views
from . import endpoints

schema_view = get_schema_view(
    openapi.Info(
        title="StoreMaster API Documentation",
        default_version='v1',
        description="""This API provides seamless access to the StoreMaster system's 
        functionalites for managing products, inventory, orders, purchases, 
        and user accounts of both employees and customers""",
        contact=openapi.Contact(email="jmjohnson1578@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "Stores"

urlpatterns = [
    path('stores', views.index,name='index'),
    path('search_for_store', views.search_for_stores, name='search_for_store'),
    path('register_store',views.register_store,name='register_store'),
    path('get-all-managers',views.get_all_managers,name='get-all-managers'),
    path('get-all-available-managers', views.get_all_available_managers,name='get-all-available-managers'),
    path('register_store_manager',views.register_store_page_2,name='register_store_page_2'),
    path('manage_store',views.manage_store,name='manage_store'),
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
    path('view_purchase', views.view_purchase, name='view_purchase'),
    path('view_shipment/<int:shipment_id>',views.view_shipment,name='view_shipment'),
    path('view_all_shipments/<int:store_id>',views.view_all_shipments,name='view_all_shipments'),
    path('add_new_shipment/<int:store_id>',views.add_new_shipment,name='add_new_shipment'),
    path('view_order', views.view_order,name='view_order'),
    path('employee_view_order/<int:order_id>',views.employee_view_order,name='employee_view_order'),
    path('stock_product_from_shipment/<int:shipment_id>/<int:product_id>',views.stock_product_from_shipment,name='stock_product_from_shipment'),
    path('stock_all_products_from_shipment/<int:shipment_id>',views.stock_all_products_from_shipment,name='stock_all_products_from_shipment'),
    path('confirm_new_order/<int:customer_id>',views.confirm_new_order,name='confirm_new_order'),

    path('api/store', endpoints.store_endpoint),
    path('api/store/<int:store_id>', endpoints.store_endpoint),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]   