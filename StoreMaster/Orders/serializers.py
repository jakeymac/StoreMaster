from rest_framework import serializers
from .models import *
from Accounts.serializers import CustomerInfoSerializer
from Stores.serializers import StoreSerializer

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime("%m-%d-%Y")
        else:
            return None

class OrderSerializer(serializers.ModelSerializer):
    customer_id = CustomerInfoSerializer()
    store = StoreSerializer()
    shipping_line_two = serializers.CharField(required=False)
    order_date = CustomDateField()
    class Meta:
        model = Order
        fields = ['order_id', 'store', 'customer_id', 'order_date','order_total','shipping_address'
                  'shipping_line_two', 'shipping_city', 'shipping_state', 'shipping_zip']


