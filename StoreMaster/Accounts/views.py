from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import UserRegistrationForm,UserSelectorForm,EditManagerForm,EditAdminForm, EditCustomerForm, EditEmployeeForm

from django.contrib.auth.models import User
from django import forms
from .models import *


def view_user(request, user_id):
    return HttpResponse(user_id)

def edit_user_view(request,user_id):
    #NEED TO CHECK FOR IF THE USER HAS CHANGED THE SELECTED ACCOUNT'S ACCOUNT TYPE. 
    user = User.objects.get(id=user_id)
    original_type = user.userinfo.account_type
    if original_type == "manager":
        manager_info = ManagerInfo.objects.get(user=user)
        form = EditManagerForm(instance=manager_info)

    elif original_type == "admin":
        admin_info = AdminInfo.objects.get(user=user)
        form = EditAdminForm(instance=admin_info)

    elif original_type == "employee":
        employee_info = EmployeeInfo.objects.get(user=user)
        form = EditEmployeeForm(instance=employee_info)
        
    elif original_type == "customer":
        customer_info = CustomerInfo.objects.get(user=user)
        form = EditCustomerForm(instance=customer_info) 


    if request.method == "POST": 
        #If the user hasn't changed the account type
        if request.POST["account_type"] == original_type:
            if original_type == "manager":
                form = EditManagerForm(request.POST,instance=manager_info)
                
            elif original_type == "admin":
                form = EditAdminForm(request.POST,instance=admin_info)
            
            elif original_type == "employee":
                form = EditEmployeeForm(request.POST,instance=employee_info)
            
            elif original_type == "customer":
                form = EditCustomerForm(request.POST, instance=customer_info)
            
            if form.is_valid():
                form.save()
                return HttpResponse("Success")
                #return redirect("Accounts:view_,)
            else:
                return HttpResponse("ERROR HERE")
            
        else:
            if request.POST["account_type"] == "manager":
                form = EditManagerForm(request.POST)

            
    


    
    if request.method == "POST":
        if request.POST["account_type"] == "manager":
            manager_instance = ManagerInfo.objects.get()
            #form = EditManagerForm(request.POST,instance=)

        elif request.POST["account_type"] == "admin":
            form = EditAdminForm(request.POST)

        elif request.POST["account_type"] == "employee":
            form = EditEmployeeForm(request.POST)

        elif request.POST["account_type"] == "customer":
            form = EditCustomerForm(request.POST)

        if form.is_valid():
            form.save()
            
        else:
            print(form.errors)
            return HttpResponse("ERROR EDITING USER")

        return redirect("view_user",user_id)
    
    else:
        user = User.objects.get(id=user_id)
        if user.userinfo.account_type == "manager":
            manager_info = ManagerInfo.objects.get(user=user)
            form = EditManagerForm(instance=manager_info)

        elif user.userinfo.account_type == "admin":
            admin_info = AdminInfo.objects.get(user=user)
            form = EditAdminForm(instance=admin_info)

        elif user.userinfo.account_type == "employee":
            employee_info = EmployeeInfo.objects.get(user=user)
            form = EditEmployeeForm(instance=employee_info)
            
        elif user.userinfo.account_type == "customer":
            customer_info = CustomerInfo.objects.get(user=user)
            form = EditCustomerForm(instance=customer_info)

        return render(request,"edit_user.html",context={"user":user,"form":form})

def select_user_view(request):
    if request.method=="POST":
        return redirect("Accounts:edit_user", user_id=request.POST["account"])
    else:
        form = UserSelectorForm()
        return render(request,"user_selector_for_edit.html",context={"form":form})
    

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
    if request.method == "POST":
        new_form = UserRegistrationForm(request.POST)
        if new_form.is_valid():
            username = new_form.cleaned_data["username"]
            password = new_form.cleaned_data["password"]
            email_address = new_form.cleaned_data["email_address"]
            address = new_form.cleaned_data["address"]
            
            first_name = new_form.cleaned_data["first_name"]
            last_name = new_form.cleaned_data["last_name"]
            other_information = new_form.cleaned_data["other_information"]
            birthday = new_form.cleaned_data["birthday"]

            store = new_form.cleaned_data["store"]
            if store:
                store_object = Store.objects.get(store_id=store.store_id)
            else:
                store_object = None
                
            user_type = new_form.cleaned_data["user_type"]

            if User.objects.filter(username=username).exists():
                return render(request,"register_user.html",{"error_message":"Username already taken", "form":new_form})
                #raise forms.ValidationError("This username is already in use")
            
            elif  User.objects.filter(email=email_address).exists():
                return render(request,"register_user.html",{"error_message":"Email already in use","form":new_form})
                #raise forms.ValidationError("This email is already in use")
            
            else:
                user = User(username=username,
                            password=make_password(password), 
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
                                                store=store_object,
                                                account_type="employee")
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
                                                store=store_object,
                                                account_type="manager")
                    new_manager.save()
                    
                #TODO add verification to create an admin account
                elif user_type == "admin":
                    new_admin = AdminInfo(user=user,
                                                username=username,
                                                password=password,
                                                email_address=email_address,
                                                address=address,
                                                first_name=first_name,
                                                last_name=last_name,
                                                other_information=other_information,
                                                birthday=birthday,
                                                store=store_object,
                                                account_type="admin")
                    new_admin.save()
                #customer
                else:
                    pass

                return HttpResponse("Successssssssss")
        else:
            
            return HttpResponse(f"INVALID FORM,\n{new_form.errors}")
    
        
    else:
        clean_form = UserRegistrationForm()
    
        return render(request,"register_user.html",{'form':clean_form})
    

    