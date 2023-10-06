from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm

from django.contrib.auth.models import User
from django import forms
from .models import *

# Create your views here.
def index(request):
    return render(request, "login_registration_home.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("Successfully Logged in")
        else:
            return render(request,"login_user.html",{"error_message":"Invalid"})
    else:

        return render(request,"login_user.html",{})


def register_user(request):
    stores = Store.objects.all()
    context = {"stores":stores}
    if request.method == "POST":
        new_form = RegistrationForm(request.POST)
        if new_form.is_valid():
            username = new_form.cleaned_data["username"]
            password = new_form.cleaned_data["password"]
            email_address = new_form.cleaned_data["email_address"]
            address = new_form.cleaned_data["address"]
            
            first_name = new_form.cleaned_data["first_name"]
            last_name = new_form.cleaned_data["last_name"]
            other_information = new_form.cleaned_data["other_information"]
            birthday = new_form.cleaned_data["birthday"]

            store_id = new_form.cleaned_data["store_id"]
            store_object = Store.objects.get(store_id=store_id)
            user_type = new_form.cleaned_data["user_type"]


            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username is already in use")
            elif  User.objects.filter(email=email_address).exists():
                raise forms.ValidationError("This email is already in use")
            
            else:
                user = User(username=username,
                            password=password, 
                            email=email_address)
                user.save()

                #TODO add verification to create an employee account
                if user_type == "employee":
                    new_employee = EmployeeInfo(user=user,
                                                username=username,
                                                password=password,
                                                email_address=email_address,
                                                address=address,
                                                first_name=first_name,
                                                last_name=last_name,
                                                other_information=other_information,
                                                birthday=birthday,
                                                store=store_object)
                    new_employee.save()

                #TODO add verification to create a manager account
                elif user_type == "manager":
                    new_manager = ManagerInfo(user=user,
                                                username=username,
                                                password=password,
                                                email_address=email_address,
                                                address=address,
                                                first_name=first_name,
                                                last_name=last_name,
                                                other_information=other_information,
                                                birthday=birthday,
                                                store=store_object)
                    new_manager.save()
                    
                #TODO add verification to create an admin account
                elif user_type == "admin":
                    new_admin = EmployeeInfo(user=user,
                                                username=username,
                                                password=password,
                                                email_address=email_address,
                                                address=address,
                                                first_name=first_name,
                                                last_name=last_name,
                                                other_information=other_information,
                                                birthday=birthday,
                                                store=store_object)
                    new_admin.save()
                #customer
                else:
                    pass

                return HttpResponse("Successssssssss")
        else:
            
            return HttpResponse(f"INVALID FORM,\n{new_form.errors}")
    
        
    else:
        clean_form = RegistrationForm()
    
        return render(request,"register_user.html",{'form':clean_form})
    

    