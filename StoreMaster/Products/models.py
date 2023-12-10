from django.db import models
from Stores.models import Store
from Accounts.models import CustomerInfo, ManagerInfo
from Orders.models import Order
from Purchases.models import Purchase
from Shipments.models import Shipment

from django.core.mail import send_mail

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
    low_stock_quantity = models.IntegerField()

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

    def update_stock(self,quantity):
        self.product_stock += quantity
        self.save()
        
        if self.product_stock <= 0 or self.product_stock <= self.low_stock_quantity:
            if self.product_stock <= 0:
                message = f"Product ID - {self.product_id} - {self.product_name} is now out of stock. Please log in to StoreMaster and make arrangements for new stock to be shipped to your location. "
            elif self.product_stock <= self.low_stock_quantity:
                message = f"Product ID - {self.product_id} - {self.product_name} is low on stock, currently at {self.product_stock}. Please log in to StoreMaster and make arrangements for more stock to be shipped to your location."
            
            store = self.store
            email_list = ManagerInfo.objects.filter(store=store, stock_notifications=True).values_list('email_address',flat=True)
            print(email_list)
                
            subject = 'StoreMaster Stock Notification'
            from_address = 'storemastersystem@gmail.com'
            try:
                send_mail(subject,
                        message,
                        from_address,
                        email_list,
                        fail_silently=True
                        )
            except Exception as e:
                print(f"an error occurred: \n{e}")
                

        #TODO add here to check for stock levels needing to be updated. iE if stock hits zero, alert the manager(s)( could add option for managers to
        #  have notifications on or off. If the stock hits a certain level? 
        # )

class ProductInShipment(models.Model):
    shipment = models.ForeignKey(Shipment,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20) #Placed into inventory/stocked already or not. 

class ProductInCart(models.Model):
    customer_id = models.ForeignKey(CustomerInfo,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

class ProductInOrder(models.Model):
    order_info_object = models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

class ProductInPurchase(models.Model):
    purchase_info_object = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()