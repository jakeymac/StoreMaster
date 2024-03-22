from rest_framework import serializers
from .models import *

from Stores.serializers import StoreSerializer

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime("%m-%d-%Y")
        else:
            return None

class ShipmentSerializer(serializers.ModelSerializer):
    destination_store = StoreSerializer()
    shipment_status = serializers.CharField(required=False)
    shipment_tracking_history = serializers.CharField(required=False)
    shipment_tracking_link = serializers.CharField(required=False)
    shipment_tracking_num = serializers.CharField(required=False)
    shipment_freight_company = serializers.CharField(required=False)

    shipped_date = CustomDateField()
    expected_date = CustomDateField()

    class Meta:
        model = Shipment
        fields = ['shipment_id', 'shipment_origin', 'destination_store','shipped_date',
                  'expected_date','shipment_status','shipment_tracking_history','shipment_tracking_link',
                  'shipment_tracking_num','shipment_freight_company']