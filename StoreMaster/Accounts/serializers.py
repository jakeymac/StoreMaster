from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from Stores.serializers import StoreSerializer

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email']

    
class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime("%m-%d-%Y")
        else:
            return None

class BaseAccountInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    store = StoreSerializer()
    email_address = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    line_two = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zip = serializers.CharField(required=False)
    other_information = serializers.CharField(required=False)
    birthday = CustomDateField(required=False)

    class Meta:
        fields = ['user', 'first_name', 'last_name', 'email_address', 'address', 
                  'line_two', 'city', 'state', 'zip', 'store', 'username', 'password', 
                  'other_information','birthday','account_type']

class CustomerInfoSerializer(BaseAccountInfoSerializer):
    class Meta(BaseAccountInfoSerializer.Meta):
        model = CustomerInfo
        fields = BaseAccountInfoSerializer.Meta.fields


class EmployeeInfoSerializer(BaseAccountInfoSerializer):
    class Meta(BaseAccountInfoSerializer.Meta):
        model = EmployeeInfo
        fields = BaseAccountInfoSerializer.Meta.fields
        

class ManagerInfoSerializer(BaseAccountInfoSerializer):
    class Meta:
        model = ManagerInfo
        fields = BaseAccountInfoSerializer.Meta.fields + ['stock_notifications']


class AdminInfoSerializer(BaseAccountInfoSerializer):
    class Meta:
        model = AdminInfo
        fields = BaseAccountInfoSerializer.Meta.fields