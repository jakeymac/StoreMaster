from django import forms
from django.forms.widgets import DateInput
from Stores.models import Store
from django.contrib.auth.models import User
from .models import ManagerInfo, AdminInfo, EmployeeInfo, CustomerInfo


class UserSelectorForm(forms.Form):
    account = forms.ModelChoiceField(queryset=User.objects.all(),empty_label="Select an account")

class EditManagerForm(forms.ModelForm):
    class Meta:
        model = ManagerInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }

class EditAdminForm(forms.ModelForm):
    class Meta:
        model = AdminInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }

class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }
class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = "__all__"
        widgets={
            "user":forms.HiddenInput(),
            "birthday":forms.SelectDateWidget(years=range(1900, 2030))
        }
        
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
    
    store = forms.ModelChoiceField(required=False,queryset=Store.objects.all(), empty_label="Store Location", label="Select a Store Location")

    user_types = [("employee","Employee"), ("manager","Manager"),("admin","Admin")]
    user_type = forms.ChoiceField(required=False,label="Account Type", choices = user_types)

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username = cleaned_data.get("username")).exists() and User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("That username and that email address are already in use")
        
        if User.objects.filter(username = cleaned_data.get("username")).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        if User.objects.filter(email = cleaned_data.get("email_address")).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        
        return cleaned_data