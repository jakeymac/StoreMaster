from django import forms
from django.forms.widgets import DateInput
from Stores.models import Store
from django.contrib.auth.models import User
from .models import ManagerInfo, AdminInfo, EmployeeInfo, CustomerInfo


class CustomerLoginForm(forms.Form):
    username = forms.CharField(required=True,label="Username",max_length=30)
    password = forms.CharField(required=True,widget=forms.PasswordInput,label="Password,max_length=30")
    

class UserSelectorForm(forms.Form):
    account = forms.ModelChoiceField(queryset=User.objects.all(),empty_label="Select an account")

class BaseEditForm(forms.ModelForm):
    class Meta:
        abstract = True

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        
        try:
            if self.instance.user:
                if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
                    self.add_error("username","Username already exists")
                if User.objects.filter(email=email).exclude(id=self.instance.user_id).exists():
                    self.add_error("email","Email address already in use")
            

        except:
            #Additional verification can be done here - this function will need ot be overrided: could make 
            #username and email verification seperate functions to inherit in each form.
            pass
            
        return cleaned_data

class EditManagerForm(BaseEditForm):
    class Meta:
        model = ManagerInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }

class EditAdminForm(BaseEditForm):
    class Meta:
        model = AdminInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }

class EditEmployeeForm(BaseEditForm):
    class Meta:
        model = EmployeeInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }
class EditCustomerForm(BaseEditForm):
    class Meta:
        model = CustomerInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }
        
class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(required=True,label="First Name",max_length=35)
    last_name = forms.CharField(required=True,label="Last Name",max_length=50)
    email_address = forms.EmailField(required=True,label="Email Address")
    address = forms.CharField(required=False,label="Address",max_length=200)
    line_two = forms.CharField(required=False,label="Address Line Two",max_length=40)
    city = forms.CharField(required=False,label="City",max_length=50)
    state = forms.CharField(required=False,label="State",max_length=50)
    zip = forms.IntegerField(required=False,label="ZIP Code",max_value=999999)
    username = forms.CharField(required=True,label="Username",max_length=30)
    password = forms.CharField(required=True, widget=forms.PasswordInput,label="Password",max_length=30)
    other_information = forms.CharField(required=False,label="Other Information",max_length = 1000)
    
    birthday = forms.DateField(widget=DateInput(attrs={'type':'date'}),label="Birthday")
    
    account_type = "customer"

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username = cleaned_data.get("username")).exists() and User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("That username and that email address are already in use")
        
        if User.objects.filter(username = cleaned_data.get("username")).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        if User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        
        return cleaned_data
    
class StoreRegistrationManagerForm(forms.Form):
    first_name = forms.CharField(required=True,label="First Name",max_length=35)
    last_name = forms.CharField(required=True,label="Last Name",max_length=50)
    email_address = forms.EmailField(required=True,label="Email Address")
    address = forms.CharField(required=False,label="Address",max_length=200)
    line_two = forms.CharField(required=False,label="Address Line Two",max_length=40)
    city = forms.CharField(required=False,label="City",max_length=50)
    state = forms.CharField(required=False,label="State",max_length=50)
    zip = forms.IntegerField(required=False,label="ZIP Code",max_value=999999)
    username = forms.CharField(required=True,label="Username",max_length=30)
    password = forms.CharField(required=True, widget=forms.PasswordInput,label="Password",max_length=30)
    other_information = forms.CharField(required=False,label="Other Information",max_length = 1000)
    stock_notifications = forms.BooleanField(required=True,label="Receive Stock Notifications")

    birthday = forms.DateField(widget=DateInput(attrs={'type':'date'}),label="Birthday")

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username = cleaned_data.get("username")).exists() and User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("That username and that email address are already in use")
        
        if User.objects.filter(username = cleaned_data.get("username")).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        if User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        
        return cleaned_data


#For validating and cleaning registration data
class EmployeeRegistrationForm(forms.Form):
    first_name = forms.CharField(required=True,label="First Name",max_length=35)
    last_name = forms.CharField(required=True,label="Last Name",max_length=50)
    email_address = forms.EmailField(required=True,label="Email Address")
    address = forms.CharField(required=False,label="Address",max_length=200)
    line_two = forms.CharField(required=False,label="Address Line Two",max_length=40)
    city = forms.CharField(required=False,label="City",max_length=50)
    state = forms.CharField(required=False,label="State",max_length=50)
    zip = forms.IntegerField(required=False,label="ZIP Code",max_value=999999)
    username = forms.CharField(required=True,label="Username",max_length=30)
    password = forms.CharField(required=True, widget=forms.PasswordInput,label="Password",max_length=30)
    other_information = forms.CharField(required=False,label="Other Information",max_length = 1000)
    stock_notifications = forms.BooleanField(required=True,label="Receive notifications for stock levels")

    birthday = forms.DateField(widget=DateInput(attrs={'type':'date'}),label="Birthday")
    
    store = forms.ModelChoiceField(required=True,queryset=Store.objects.all(), empty_label="Store Location", label="Select a Store Location")

    account_types = [("employee","Employee"), ("manager","Manager"),("admin","Admin")]
    account_type = forms.ChoiceField(required=False,label="Account Type", choices = account_types)

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username = cleaned_data.get("username")).exists() and User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("That username and that email address are already in use")
        
        if User.objects.filter(username = cleaned_data.get("username")).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        if User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        
        return cleaned_data