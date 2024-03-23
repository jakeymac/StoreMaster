from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from Stores.serializers import StoreSerializer

class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            return value.strftime("%m-%d-%Y")
        else:
            return None

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'password','email']

    def run_validation(self, attrs):
        print("Running validationg for user serializer")
        user_id = attrs.get('id')
        new_username = attrs.get('username')
        new_email = attrs.get('email')
        
        new_errors = []
        if new_username:
            if User.objects.filter(username=new_username).exclude(pk=user_id).exists():
                new_errors.append("username already exists")
                
        if new_email:
            if User.objects.filter(email=new_email).exclude(pk=user_id).exists():
                new_errors.append("email already exists")

        if new_errors:
            if len(new_errors) == 1:
                if new_errors[0] == "username already exists":
                    raise serializers.ValidationError("Username is already taken")
                elif new_errors[0] == "email already exists": 
                    raise serializers.ValidationError("Email is already taken")
            else:
                raise serializers.ValidationError("Username and email are already taken")
            
        return attrs

class BaseAccountInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    birthday = CustomDateField()

    class Meta:
        fields = ['user', 'first_name', 'last_name', 'email_address', 'address', 
                  'line_two', 'city', 'state', 'zip', 'store', 'username', 'password', 
                  'other_information','birthday','account_type']

    def run_validation(self, attrs):
        print("running validation")
        if 'user' in attrs:
            user_data = attrs['user']
            new_username = user_data.username

            already_exists = User.objects.filter(username=new_username).exclude(pk=user_data.id).exists()
            if already_exists:
                print("Already existsssss")
                raise serializers.ValidationError("Username is already taken blah blah")
        
            new_email = user_data.email
            already_exists = User.objects.filter(email=new_email).exclude(pk=user_data.id).exists()
            if already_exists:
                print("Already existssss")
                raise serializers.ValidationError("Email is already taken blah blah")

        return attrs

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