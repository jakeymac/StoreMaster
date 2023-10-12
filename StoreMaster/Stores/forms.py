from django import forms
from django.forms.widgets import DateInput
from Accounts.models import ManagerInfo

class StoreRegistrationForm(forms.Form):
    store_name = forms.CharField(required=True,label="Store Name",max_length=50)
    address = forms.CharField(required=True,label="Address",max_length=200)
    line_two = forms.CharField(required=True,label="Address Line Two",max_length=40)
    city = forms.CharField(required=True,label="City",max_length=50)
    state = forms.CharField(required=True,label="State",max_length=50)
    zip = forms.IntegerField(required=True,label="ZIP Code",max_value=999999)

    manager = forms.ModelChoiceField(required=True,queryset=ManagerInfo.objects.all(), empty_label="Select a manager", label="Select a manager for the new location")
    
    first_name = forms.CharField(required=False,label="First Name",max_length=35)
    last_name = forms.CharField(required=False,label="Last Name",max_length=50)
    email_address = forms.EmailField(required=False,label="Email Address")
    address = forms.CharField(required=False,label="Address",max_length=200)
    line_two = forms.CharField(required=False,label="Address Line Two",max_length=40)
    city = forms.CharField(required=False,label="City",max_length=50)
    state = forms.CharField(required=False,label="State",max_length=50)
    zip = forms.IntegerField(required=False,label="ZIP Code",max_value=999999)
    username = forms.CharField(required=False,label="Username",max_length=30)
    password = forms.CharField(required=False, widget=forms.PasswordInput,label="Password",max_length=30)
    other_information = forms.CharField(required=False,label="Other Information",max_length = 1000)
    birthday = forms.DateField(required=False,widget=DateInput(attrs={'type':'date'}),label="Birthday")