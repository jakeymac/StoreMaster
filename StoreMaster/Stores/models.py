from django.db import models
from django.core.validators import MaxValueValidator
from Products.models import *

# Create your models here.


# Create your models here.

class Store(models.Model):
    store_id = models.AutoField(primary_key = True)
    store_name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    line_two = models.CharField(max_length=35,blank=True,null=True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 20)
    zip = models.IntegerField(validators=[MaxValueValidator(999999)])

    def __str__(self):
        return f"{self.store_name} - {self.address}, {self.city}, {self.state}"

    def get_store_id(self):
        return self.store_id

    def get_store_name(self):
        return self.store_name
    
    def get_location(self):
        if self.line_two:
            return f"{self.address} {self.line_two} {self.zip} {self.city}, {self.state}"
        else:
            return f"{self.address} {self.zip} {self.city}, {self.state}"
    
    def get_address(self):
        return self.address
    
    
    def set_address(self, address):
        self.address = address

class StoreHasStock(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    store = models.OneToOneField(Store,on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.product} at {self.store}"