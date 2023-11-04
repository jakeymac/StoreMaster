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

    def clean(self):
        cleaned_data = super().clean()
        #Valid store information fields first
        print("Running clean now, PRE VALIDATION")
        print(f"Checking {cleaned_data.get('store_name')}")
        print(f"List: {Store.objects.values_list('store_name')} ")



        if Store.objects.filter(
            store_name = cleaned_data.get('store_name'),
            address = cleaned_data.get('store_address'),
            line_two = cleaned_data.get('store_line_two'),
            zip = cleaned_data.get('store_zip'),
            city = cleaned_data.get('store_city'),
            state = cleaned_data.get('store_state'),
        ).exists():
            raise forms.ValidationError("A store with name already exists at that address")
        
        """if is_store_name_exists(cleaned_data.get('store_name')):

        if cleaned_data.get("store_name") in Store.objects.values_list("store_name",flat=True):
            #Retreive all stores that have this name to make sure there isn't one at this location already
            stores = Store.objects.filter(store_name=cleaned_data.get('store_name'))
            locations = [store.get_location() for store in stores]
            print("Running clean on store registration form")
            print(stores)
            if cleaned_data.get("store_line_two"):
                if f"{cleaned_data.get('store_address')} {cleaned_data.get('store_line_two')} {cleaned_data.get('store_zip')} {cleaned_data.get('store_city')}, {cleaned_data.get('store_state')}" in locations:
                    print("\n\n\nISSUE HERE \n\n\n")
                    
                    
            else:
                if f"{cleaned_data.get('store_address')} {cleaned_data.get('store_zip')} {cleaned_data.get('store_city')}, {cleaned_data.get('store_state')}" in locations:
                    print("\n\n\nISSUE HERE \n\n\n")
                    raise forms.ValidationError("A store with name already exists at that address")



            #raise ValidationError("A store with that name already exists")

        #validate manager information if it's been provided"""
        return cleaned_data
