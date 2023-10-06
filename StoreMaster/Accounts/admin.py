from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserInfo)
admin.site.register(AdminInfo)
admin.site.register(ManagerInfo)
admin.site.register(EmployeeInfo)
admin.site.register(CustomerInfo)