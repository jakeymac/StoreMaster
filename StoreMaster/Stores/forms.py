from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from Accounts.models import UserInfo, ManagerInfo
from .models import Store
from Accounts.forms import UserRegistrationForm



class StoreRegistrationForm(forms.Form):
    store_name = forms.CharField(required=True,label="Store Name",max_length=50)
    store_address = forms.CharField(required=True,label="Address",max_length=200)
    store_line_two = forms.CharField(required=True,label="Address Line Two",max_length=40)
    store_city = forms.CharField(required=True,label="City",max_length=50)
    store_state = forms.CharField(required=True,label="State",max_length=50)
    store_zip = forms.IntegerField(required=True,label="ZIP Code",max_value=999999)

    # manager = forms.ModelChoiceField(required=False,queryset=ManagerInfo.objects.all(),empty_label="Select a manager", label="Select a manager for the new location",blank=True)
    
    # manager_first_name = forms.CharField(required=False,label="First Name",max_length=35)
    # manager_last_name = forms.CharField(required=False,label="Last Name",max_length=50)
    # manager_email_address = forms.EmailField(required=False,label="Email Address")
    # manager_address = forms.CharField(required=False,label="Address",max_length=200)
    # manager_line_two = forms.CharField(required=False,label="Address Line Two",max_length=40)
    # manager_city = forms.CharField(required=False,label="City",max_length=50)
    # manager_state = forms.CharField(required=False,label="State",max_length=50)
    # manager_zip = forms.IntegerField(required=False,label="ZIP Code",max_value=999999)
    # manager_username = forms.CharField(required=False,label="Username",max_length=30)
    # manager_password = forms.CharField(required=False, widget=forms.PasswordInput,label="Password",max_length=30)
    # manager_other_information = forms.CharField(required=False,label="Other Information",max_length = 1000)
    # manager_birthday = forms.DateField(required=False,widget=DateInput(attrs={'type':'date'}),label="Birthday")

    def clean(self):
        cleaned_data = super().clean()
        #Valid store information fields first
        if cleaned_data.get("store_name") in Store.objects.values_list("store_name",flat=True):
            #Retreive all stores that have this name to make sure there isn't one at this location already
            stores = Store.objects.filter(store_name=cleaned_data.get('store_name'))
            locations = [store.get_location() for store in stores]
            if cleaned_data.get("store_line_two"):
                if f"{cleaned_data.get('store_address')} {cleaned_data.get('store_line_two')} {cleaned_data.get('store_zip')} {cleaned_data.get('store_city')}, {cleaned_data.get('store_state')}" in locations:
                    raise forms.ValidationError("A store with name already exists at that address")
            else:
                if f"{cleaned_data.get('store_address')} {cleaned_data.get('store_zip')} {cleaned_data.get('store_city')}, {cleaned_data.get('store_state')}" in locations:
                    raise forms.ValidationError("A store with name already exists at that address")
                
            if not self.manager:
                if User.objects.filter(username=cleaned_data.get("manager_username")).exists():
                    raise forms.ValidationError("This username is already in use")
                if User.objects.filter(email=cleaned_data.get("manager_email_address")).exists():
                    raise forms.ValidationError("This username is already in use")


            #raise ValidationError("A store with that name already exists")

        #validate manager information if it's been provided
        return cleaned_data
