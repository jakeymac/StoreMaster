from django.db import models

# Create your models here.
from django.db import models
from Stores.models import Store
from Accounts.models import EmployeeInfo, ManagerInfo, CustomerInfo

# Create your models here.
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key = True)
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    employee_id = models.OneToOneField(EmployeeInfo, on_delete=models.CASCADE, related_name="employee",null=True)
    manager_id = models.OneToOneField(ManagerInfo,on_delete=models.CASCADE,related_name="manager",null=True)
    customer_id = models.OneToOneField(CustomerInfo,on_delete=models.CASCADE, related_name="customer")
    purchase_date = models.DateTimeField()
    purchase_total = models.FloatField() #could update this model for tax registration
    items = models.CharField(max_length=800)

    def get_purchase_id(self):
        return self.purchase_id

    def get_store(self):
        return self.store
    
    def set_store(self, store):
        self.store = store

    def get_employee_id(self):
        return self.employee_id
    
    def set_employee_id(self, employee):
        self.employee_id = employee

    def get_customer_id(self):
        return self.customer_id
    
    def set_customer_id(self,customer):
        self.customer_id = customer 

    def get_purchase_date(self):
        return self.purchase_date
    
    def set_purchase_date(self, date):
        self.purchase_date = date

    def get_total(self):
        return self.purchase_total
    
    def set_total(self, total):
        self.purchase_total = total

    def get_items(self):
        return self.items
    
    def set_items(self, items):
        self.items = items
