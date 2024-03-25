from rest_framework import serializers
from .models import *
from Stores.serializers import StoreSerializer
from Shipments.serializers import ShipmentSerializer
from Accounts.serializers import CustomerInfoSerializer
from Orders.serializers import OrderSerializer
from Purchases.serializers import PurchaseSerializer

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    product_image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['product_id', 'store', 'product_stock','product_image','product_name',
                  'product_description','product_price','product_location','low_stock_quantity','is_active']

class ProductInShipmentSerializer(serializers.ModelSerializer):
    shipment = ShipmentSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductInShipment
        fields = ['shipment','product','quantity','status']

class ProductInCartSerializer(serializers.ModelSerializer):
    customer_id = CustomerInfoSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductInCart
        fields = ['customer_id','product','quantity']

class ProductInOrderSerializer(serializers.ModelSerializer):
    order_info_object = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductInOrder
        fields = ['order_info_object', 'product', 'quantity']

class ProductInPurchaseSerializer(serializers.ModelSerializer):
    purchase_info_object = PurchaseSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductInPurchase
        fields = ['purchase_info_object', 'product', 'quantity']


