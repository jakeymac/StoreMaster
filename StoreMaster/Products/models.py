from django.db import models
from Stores.models import Store

def product_image_path(instance, filename):
    return f'stores/{instance.store.store_id}/products/{instance.product_id}/{filename}'


# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    product_stock = models.IntegerField()
    product_image = models.ImageField(null=True,blank=True,upload_to=product_image_path)
    product_name = models.CharField(max_length=150)
    product_description = models.CharField(max_length=1000)
    product_price = models.FloatField()
    product_location = models.CharField(max_length=10)

    def __str__(self):
        return self.product_name
    
    def get_name(self):
        return self.product_name
    
    def set_name(self, name):
        self.product_name = name

    def get_product_id(self):
        return self.product_id
    
    def get_store(self):
        return self.store
    
    def get_description(self):
        return self.product_description
    
    def set_description(self,description):
        self.product_description = description

    def get_price(self):
        return self.product_price
    
    #TODO add a sale option to this model to display as well
    def set_price(self,price):
        self.product_price = price

    def get_product_image(self):
        return self.product_image
    
    def set_product_image(self,image):
        self.product_image = image

    def get_product_location(self):
        return self.product_location
    
    def set_product_location(self,location):
        self.product_location = location

    def get_product_stock(self):
        return self.product_stock
    
    def set_product_stock(self, stock):
        self.product_stock = stock

    #TODO add verification for increase - make sure it doesn't go past a limit(could add a field for maximum stock?)
    def add_product_stock(self, increase):
        self.product_stock += increase

    #TODO add verification for remove - can't go past 0 
    def remove_product_stock(self, decrease):
        self.product_stock -= decrease
