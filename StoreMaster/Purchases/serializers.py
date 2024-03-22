from rest_framework import serializers
from .models import *

from Accounts.models import CustomerInfo, EmployeeInfo, ManagerInfo, AdminInfo
from Accounts.serializers import (CustomerInfoSerializer, EmployeeInfoSerializer, 
                                  ManagerInfoSerializer, AdminInfoSerializer)

from Stores.serializers import StoreSerializer

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime("%m-%d-%Y")
        else:
            return None

class PurchaseSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    customer_id = CustomerInfoSerializer()
    employee_id = serializers.PrimaryKeyRelatedField(queryset=EmployeeInfo.objects.all(), required=False)
    manager_id = serializers.PrimaryKeyRelatedField(queryset=ManagerInfo.objects.all(), required=False)
    admin_id = serializers.PrimaryKeyRelatedField(queryset=AdminInfo.objects.all(), required=False)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=CustomerInfo.objects.all(), required=False)

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    purchase_date = CustomDateField()

    def validate(self, data):
        filled_fields = [field for field in ['employee_id', 'manager_id', 'admin_id'] if data.get(field)]
        if len(filled_fields) != 1:
            raise serializers.ValidationError("Exactly one store official field should be filled")
        return data 

    class Meta:
        model = Purchase
        fields = ['purchase_id','store', 'employee_id', 'manager_id', 'admin_id', 
                  'customer_id', 'first_name', 'last_name', 'purchase_date']