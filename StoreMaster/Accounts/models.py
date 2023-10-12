from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from Stores.models import Store


# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length = 50)
    email_address = models.CharField(max_length = 75, null=True, blank=True,unique=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    line_two = models.CharField(max_length=35,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=35,null=True,blank=True)
    zip = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(999999)])
    store = models.OneToOneField(Store,null=True,blank=True,on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True,blank=True,unique=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    other_information = models.CharField(max_length = 1000,null=True,blank=True)
    birthday = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.username
    
    def get_user_type(self):
        return self.user_type
    
    def set_user_type(self, type):
        self.user_type = type

    def get_first_name(self):
        return self.first_name
    
    def set_first_name(self, name):
        self.first_name = name

    def get_last_name(self):
        return self.last_name
    
    def set_last_name(self, name):
        self.last_name = name

    def get_email(self):
        return self.email_address
    
    def set_email(self, email):
        self.email_address = email
    
    def get_address(self):
        return self.address
    
    def set_address(self, address):
        self.address = address

    def get_store_id(self):
        return self.store_id
    
    def set_store_id(self, store):
        self.store_id = store

    def get_username(self):
        return self.username
    
    def set_username(self, username):
        self.username = username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_other_information(self):
        return self.other_information
    
    def set_other_information(self,info):
        self.other_information = info

    def get_birthday(self):
        return self.birthday
    
    def set_birthday(self, birthday):
        self.birthday = birthday


class AdminInfo(UserInfo):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class ManagerInfo(UserInfo):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployeeInfo(UserInfo):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CustomerInfo(UserInfo):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"