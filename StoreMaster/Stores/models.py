from django.db import models
from django.core.validators import MaxValueValidator

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

    def to_dict(self):
        return {"store_id": self.store_id,
                "store_name": self.store_name,
                "address": self.address,
                "line_two": self.line_two,
                "city": self.city,
                "state": self.state,
                "zip": self.zip}

def product_image_path(instance, filename):
    return f'stores/{instance.store.store_id}/products/{instance.product.product_id}/{filename}'