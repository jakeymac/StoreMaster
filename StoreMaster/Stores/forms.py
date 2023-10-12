from django import forms
from Accounts.models import ManagerInfo

class StoreRegistrationForm(forms.Form):
    store_name = forms.CharField(required=True,label="Store Name",max_length=50)
    address = forms.CharField(required=True,label="Address",max_length=200)
    line_two = forms.CharField(required=True,label="Address Line Two",max_length=40)
    city = forms.CharField(required=True,label="City",max_length=50)
    state = forms.CharField(required=True,label="State",max_length=50)
    zip = forms.IntegerField(required=True,label="ZIP Code",max_value=999999)

    manager = forms.ModelChoiceField(required=False,queryset=ManagerInfo.objects.all(), empty_label="Select a manager", label="Select a manager for the new location")
