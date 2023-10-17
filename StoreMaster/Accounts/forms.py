from django import forms
from django.forms.widgets import DateInput
from Stores.models import Store


#For validating and cleaning registration data
class UserRegistrationForm(forms.Form):
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
    
    store = forms.ModelChoiceField(queryset=Store.objects.all(), empty_label="Store Location", label="Select a Store Location")

    user_types = [("employee","Employee"), ("manager","Manager"),("admin","Admin")]
    user_type = forms.ChoiceField(required=True,label="Account Type", choices = user_types,)