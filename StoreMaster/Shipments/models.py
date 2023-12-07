from django.db import models
from Stores.models import Store

# Create your models here.
class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key = True)
    shipment_origin = models.CharField(max_length = 70)
    destination_store = models.ForeignKey(Store,on_delete=models.CASCADE)
    expected_date = models.DateField()
    shipment_status = models.CharField(max_length=150)
    shipment_tracking_history = models.CharField(max_length=1000)
    shipment_tracking_link = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"Shipment ID - {self.shipment_id}"

    def get_shipment_id(self):
        return self.shipment_id
    
    def get_shipment_origin(self):
        return self.shipment_origin
    
    def set_shipment_origin(self, origin):
        self.shipment_origin = origin

    def get_destination_store(self):
        return self.destination_store
    
    def set_destination_store(self, store):
        self.destination_store = store

    def get_expected_date(self):
        return self.expected_date

    def set_expected_date(self, date):
        self.expected_date = date

    def get_shipment_status(self):
        return self.shipment_status
    
    def set_shipment_status(self, status):
        self.shipment_status = status

    def get_shipment_tracking_history(self):
        return self.shipment_tracking_history
    
    def set_shipment_tracking_history(self,history):
        self.shipment_tracking_history = history

    def get_tracking_link(self):
        return self.shipment_tracking_link
    
    def set_tracking_link(self,link):
        self.shipment_tracking_link = link