from django.db import models

# Create your models here.
from django.db import models
from Stores.models import Store
from Accounts.models import EmployeeInfo, ManagerInfo, AdminInfo, CustomerInfo

# Create your models here.
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key = True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name="employee",null=True,blank=True)
    manager_id = models.ForeignKey(ManagerInfo,on_delete=models.CASCADE,related_name="manager",null=True,blank=True)
    admin_id = models.ForeignKey(AdminInfo,on_delete=models.CASCADE, related_name="admin",null=True,blank=True)
    customer_id = models.ForeignKey(CustomerInfo,on_delete=models.CASCADE, related_name="customer",null=True,blank=True)
    first_name = models.CharField(max_length=25,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    purchase_date = models.DateTimeField()
    purchase_total = models.FloatField() #could update this model for tax registration

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

