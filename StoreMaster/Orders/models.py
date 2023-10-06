from django.db import models
from django.core.validators import MaxValueValidator
from Stores.models import Store
from Accounts.models import CustomerInfo

# Create your models here.

class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomerInfo,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    destination = models.CharField(max_length = 100, null = True, blank = True)
    order_total = models.FloatField()
    items = models.CharField(max_length = 800)

    shipping_address = models.CharField(max_length=200,null=True,blank=True)
    shipping_line_two = models.CharField(max_length=35,null=True,blank=True)
    shipping_city = models.CharField(max_length=50,null=True,blank=True)
    shipping_state = models.CharField(max_length=35,null=True,blank=True)
    shipping_zip = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(999999)])

    def get_order_id(self):
        return self.order_id
    
    def get_store(self):
        return self.store
    
    def set_store(self, store):
        self.store = store

    def get_customer_id(self):
        return self.customer_id
    
    def set_customer_id(self,customer):
        self.customer_id = customer 

    def get_order_date(self):
        return self.order_date
    
    def set_order_date(self,date):
        self.order_date = date

    def get_destination(self):
        return self.destination
    
    def set_destination(self, destination):
        self.destination = destination

    def get_order_total(self):
        return self.order_total
    
    def set_order_total(self, total):
        self.order_total = total

    def get_items(self):
        return self.items
    
    def set_items(self, items):
        self.items = items
