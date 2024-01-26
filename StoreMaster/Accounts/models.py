from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from Stores.models import Store

# Create your models here.
class UserInfo(models.Model):
    
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length = 50)
    email_address = models.CharField(max_length = 75, null=True, blank=True,unique=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    line_two = models.CharField(max_length=35,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=35,null=True,blank=True)
    zip = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(999999)])
    store = models.ForeignKey(Store,null=True,blank=True,on_delete=models.CASCADE)
    username = models.CharField(max_length=30,null=True,blank=True,unique=True)
    password = models.CharField(max_length=30,null=True,blank=True)
    other_information = models.CharField(max_length = 1000,null=True,blank=True)
    birthday = models.DateField(null=True,blank=True)
    
    account_types = (('customer','Customer'),
                     ('employee','Employee'),
                     ('manager', 'Manager'),
                     ('admin','Admin'))
                     
    account_type = models.CharField(max_length=15,null=False,default="employee",choices=account_types)

    def switchModelType(self,new_account_type):
        model_dict = {"manager":ManagerInfo,
                      "admin":AdminInfo,
                      "employee":EmployeeInfo,
                      "customer":CustomerInfo}
        
        self.save()
        
        new_instance = model_dict.get(new_account_type)()
        new_instance.user = self.user
        new_instance.first_name = self.first_name
        new_instance.last_name = self.last_name
        new_instance.email_address = self.email_address
        new_instance.address = self.address
        new_instance.line_two = self.line_two
        new_instance.city = self.city
        new_instance.state = self.state
        new_instance.zip = self.zip
        new_instance.store = self.store
        new_instance.username = self.username
        new_instance.password = self.password
        new_instance.other_information = self.other_information
        new_instance.birthday = self.birthday
        new_instance.account_type = new_account_type

        new_instance.account_type = new_account_type
        return new_instance
    

    def get_full_address(self):
        return f"{self.address} {self.line_two} {self.city}, {self.state} {self.zip}"
    
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
    def __init__(self, *args, **kwargs):
        super(AdminInfo, self).__init__(*args,**kwargs)
        self.account_type = 'admin'
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ManagerInfo(UserInfo):
    stock_notifications = models.BooleanField()
    def __init__(self, *args, **kwargs):
        super(ManagerInfo, self).__init__(*args,**kwargs)
        self.account_type = 'manager'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployeeInfo(UserInfo):
    def __init__(self, *args, **kwargs):
        super(EmployeeInfo, self).__init__(*args,**kwargs)
        self.account_type = 'employee'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CustomerInfo(UserInfo):
    def __init__(self, *args, **kwargs):
        super(CustomerInfo, self).__init__(*args,**kwargs)
        self.account_type = 'customer'    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"