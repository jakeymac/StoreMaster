from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import CustomerRegistrationForm,EmployeeRegistrationForm,UserSelectorForm,EditManagerForm,EditAdminForm, EditCustomerForm, EditEmployeeForm

from django.contrib.auth.models import User
from django import forms
from .models import *


form_dict = {"manager":EditManagerForm,
             "admin":EditAdminForm,
             "employee":EditEmployeeForm,
             "customer":EditCustomerForm}
    
model_dict = {"manager":ManagerInfo,
              "admin":AdminInfo,
              "employee":EmployeeInfo,
              "customer":CustomerInfo}

def StoreMasterHome(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,"home.html",{})
    


def employee_view_customer(request,customer_id):
    customer = CustomerInfo.objects.get(user_id=customer_id)

    context={"customer":customer}
    return render(request,"employee_view_customer.html",context=context)

def employee_edit_customer(request,customer_id):
    customer = CustomerInfo.objects.get(user=User.objects.get(id=user_id))
    new_form = EditCustomerForm(instance=customer)
    context={"form":new_form}

    if request.method == "POST":
        errors = []
        edited_form = EditCustomerForm(request.POST,instance=customer)
        context["form"] = edited_formz
        if edited_form.is_valid():
            if edited_form.cleaned_data["username"] != customer.username:
                if User.objects.filter(username=edited_form.cleaned_data["username"]).exists():
                    #TODO Error for repeated username, edit User object
                    errors.append("That username is already in use")

            if edited_form.cleaned_data["email_address"] != customer.email_address:
                if edited_form.cleaned_data["email_address"] in User.objects.values_list('email_address', flat=True):
                    #TODO Error for repeated email, edit User object
                    errors.append("That email is already in use.")

            if edited_form.cleaned_data["password"] != customer.password:
                #TODO Edit user object
                customer.user.password = edited_form.cleaned_data["password"]
                customer.password = edited_form.cleaned_data["password"]
                customer.user.save()
                customer.save()


            if not errors:
                context["errors"] = errors
            else:
                edited_form.save()
                return redirect("Accounts:view_customer",user_id)
        
    return render(request,"edit_customer.html",context=context)

def employee_view_employee(request,employee_id):
    user_info = UserInfo.objects.get(user_id=employee_id)
    user = User.objects.get(userinfo=user_info)
    account_type = user.userinfo.account_type
    account = model_dict.get(account_type).objects.get(user=user)
    context = {account_type:account, "account_type":account_type} 

    return render(request,"employee_view_employee.html",context=context)
    

def view_user(request, user_id):
    if request.user.is_authenticated:
        if request.user.userinfo.account_type == "customer":
            template_start = ""
        else:
            template_start = "employee_"
    else:
        #TODO add security here to not allow just anyoen without an account to access. Update below to m
        pass
    user = User.objects.get(id=user_id)
    account_type = user.userinfo.account_type
    instance = model_dict.get(account_type).objects.get(user=user)
    context = {account_type:instance}
    if account_type == "customer":
        return render(request,template_start+"view_customer.html",context=context)
    else:
        if request.user.userinfo.account_type != "customer":
            return render(request,template_start+"view_employee.html",context=context)
        else:
            #TODO dont' allow custoemrs to access the employees' information.
            pass


def view_customer(request,user_id):
    customer = CustomerInfo.objects.get(user=User.objects.get(id=user_id))
    context = {"customer":customer}
    return render(request,"view_customer.html",context)

def view_employee(request,user_id):
    pass


def edit_customer(request,user_id):
    customer = CustomerInfo.objects.get(user=User.objects.get(id=user_id))
    new_form = EditCustomerForm(instance=customer)
    context={"form":new_form}

    if request.method == "POST":
        errors = []
        edited_form = EditCustomerForm(request.POST,instance=customer)
        context["form"] = edited_formz
        if edited_form.is_valid():
            if edited_form.cleaned_data["username"] != customer.username:
                if User.objects.filter(username=edited_form.cleaned_data["username"]).exists():
                    #TODO Error for repeated username, edit User object
                    errors.append("That username is already in use")

            if edited_form.cleaned_data["email_address"] != customer.email_address:
                if edited_form.cleaned_data["email_address"] in User.objects.values_list('email_address', flat=True):
                    #TODO Error for repeated email, edit User object
                    errors.append("That email is already in use.")

            if edited_form.cleaned_data["password"] != customer.password:
                #TODO Edit user object
                customer.user.password = edited_form.cleaned_data["password"]
                customer.password = edited_form.cleaned_data["password"]
                customer.user.save()
                customer.save()


            if not errors:
                context["errors"] = errors
            else:
                edited_form.save()
                return redirect("Accounts:view_customer",user_id)
        
    return render(request,"edit_customer.html",context=context)

def edit_user_view(request,user_id):
    #Update info on same object as long as the object is the same account_type. Also needs to check if username or password was updated
    #     
    user = User.objects.get(id=user_id)
    original_type = user.userinfo.account_type
    original_object = model_dict.get(original_type).objects.get(user=user)

    if request.method == "POST": 
        new_form = form_dict.get(request.POST.get("account_type"))(request.POST,instance=original_object)
        
        #SHOULD PERHAPS UPDATE REGISTRATION TO MAKE IT SO THAT THE USER FIELD JUST IMMEDIATELY POINTS TO THE MANGERINOF, 
        #ADMININFO, NOT A GENERIC USERINFO MODEL
        if new_form.is_valid():
            new_form.save()
            if original_type != request.POST.get("account_type"):
                new_object = original_object.switchModelType(request.POST.get("account_type"))
                print(new_object)
                original_object.delete()
                new_object.save()
            #TODO finalize error handling here and
            if request.POST["username"] != user.username:
                if not User.objects.filter(username=request.POST["username"]).exists():
                    user.username = request.POST["username"]
                    #model_dict.get(request.POST.get("account_type")).objects.get(user=user).username = request.POST["username"]
                    
            if request.POST["password"] != user.password:
            ############### MAY NEED THE MAKE PASSWORD FUNCTION #############
                user.password = request.POST["password"] 
                #model_dict.get(request.POST.get("account_type")).objects.get(user=user).password = request.POST["password"]
            
            if request.POST["email_address"] != user.email:
                if not User.objects.filter(email=request.POST["email_address"]).exists():
                    user.email = request.POST["email"]
                    #model_dict.get(request.POST.get("account_type")).objects.get(user=user).email = request.POST["email"]

            model_dict.get(request.POST.get("account_type")).objects.get(user=user).save()
            user.save()

            return redirect('Accounts:view_user',user_id=user.id)

    else:
        form_type = form_dict.get(original_type)
        form = form_type(instance=original_object)

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

def logout_customer(request):
    if "store_id" in request.session:
        store = request.session["store_id"]
    elif request.user.userinfo.store:
        store = request.user.userinfo.store.store_id

    if request.user.is_authenticated:
        logout(request)

    return redirect("Stores:store_home",store_id=store)

def logout_employee(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("Accounts:login_employee")
    

#MAY RENAME LOGIN_CUSTOMER AND HAVE A SEPERATE LOGIN_EMPLOYEE, NOT SURE YET
def login_customer(request):
    error = None
    if request.user.is_authenticated:
        if request.user.userinfo.account_type == "customer":
            if request.user.userinfo.store:
                store = request.user.userinfo.store
                
            elif "store_id" in request.session:
                store = request.session["store_id"]
            
            else:
                return HttpResponse("Error: No store found for the current account, try going to the store you're looking to access and logging in from there.")

            return redirect("Stores:store_home",store_id=store)
        
        else:
            if request.user.userinfo.store:
                return redirect("Stores:manage_store",store_id=request.user.userinfo.store.store_id)

            else:
                #Return to manage store search
                return HttpResponse("Error: No store found for the current account")

    else:
        if request.method == "POST":
            form = AuthenticationForm(request,request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)

                    if user.userinfo.store:
                        store = user.userinfo.store.store_id
                    elif "store_id" in request.session:
                        store = request.session["store_id"]
                    else:
                        return logout_customer(request)
                        return HttpResponse("No store found for that account")
                        

                    if user.userinfo.account_type == "customer":
                        return redirect("Stores:store_home",store_id=store)
                    else:
                        return redirect("logout_employee")
                        return HttpResponse("No store found for that account")
                        #add option to log out here


                else:
                    error = "Incorrect username or password"


        else:
            error = None

        form = AuthenticationForm(request)
        return render(request,"login_customer.html",{"form":form,"error":error})
    
def login_employee(request):
    error = None
    if request.user.is_authenticated:
        if request.user.userinfo.account_type == "admin":
            return redirect("Stores:admin_manage_stores")
        
        if request.user.userinfo.account_type == "customer":
            if request.user.userinfo.store:
                store = request.user.userinfo.store
                
            elif "store_id" in request.session:
                store = request.session["store_id"]
                
            else:
                return HttpResponse("Error: No store found for the current account, try going to the store you're looking to access and logging in from there.")

            return redirect("Stores:store_home",store_id=store.store_id)
        
        else:
            print(request.user.userinfo.store)
            if request.user.userinfo.store:
                return redirect("Stores:manage_store",store_id=request.session["store_id"])

            else:
                #Return to manage store search
                return HttpResponse("Error: No store found for the current account")

    else:
        if request.method == "POST":
            form = AuthenticationForm(request,request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request,user)

                    if user.userinfo.store:
                        store = user.userinfo.store
                    elif "store_id" in request.session:
                        store = request.session["store_id"]
                        # account_type = user.userinfo.account_type 
                        # print(account_type)
                        # if account_type == "admin":
                        #     store = request.session["store_id"]
                        # elif model_dict.get(account_type).objects.get(user=user).store.store_id == request.session["store_id"]:
                        #     store = request.session["store_id"]
                        # else:
                        #     return HttpResponse("No store found for that account")
                        
                        # return redirect("Stores:manage_store",store_id=store)
                
                        
                    else:
    
                        #No store ID found.
                        pass
                        #return logout_manual(request)
                        
                        
                    account_type = user.userinfo.account_type
                    if account_type == "customer":
                        return redirect("Stores:store_home",store_id=store.store_id)
                    else:
                        if account_type == "admin":
                            return redirect("Stores:admin_manage_stores")
                        elif model_dict.get(account_type).objects.get(user=user).store.store_id == store:
                            return redirect("Stores:manager_store",store_id=store.store_id)

                        #return logout_manual(request)
                        return HttpResponse("No store found for that account")
                        #add option to log out here

                else:
                    error = "Incorrect username or password"


        else:
            error = None
            
        form = AuthenticationForm(request)
        return render(request,"login_employee.html",{"form":form,"error":error})
        



def register_customer(request):
    if not "store_id" in request.session:
        return HttpResponse("Sorry, no store was found. Try visiting your desired store's website and registering there")

    if request.method == "POST":
        
        new_form = CustomerRegistrationForm(request.POST)
        if new_form.is_valid():

            username = new_form.cleaned_data["username"]
            password = new_form.cleaned_data["password"]
            email_address = new_form.cleaned_data["email_address"]
            address = new_form.cleaned_data["address"]
            
            first_name = new_form.cleaned_data["first_name"]
            last_name = new_form.cleaned_data["last_name"]
            other_information = new_form.cleaned_data["other_information"]
            birthday = new_form.cleaned_data["birthday"]

            if User.objects.filter(username=username).exists():
                return render(request,"register_customer.html",{"error_message":"Username already taken", "form":new_form})
                #raise forms.ValidationError("This username is already in use")
            
            elif  User.objects.filter(email=email_address).exists():
                return render(request,"register_customer.html",{"error_message":"Email already in use","form":new_form})
                #raise forms.ValidationError("This email is already in use")
            
            else:
                user = User(username=username,
                            password=make_password(password), 
                            email=email_address)
                user.save()


                store = Store.objects.get(store_id=request.session["store_id"])
                new_customer = CustomerInfo(user=user,
                                            username=username,
                                            password=password,
                                            email_address=email_address,
                                            address=address,
                                            first_name=first_name,
                                            last_name=last_name,
                                            other_information=other_information,
                                            birthday=birthday,
                                            account_type="customer",
                                            store=store)
                
                new_customer.save()

                return redirect(request,"Stores:home",store_id=store.store_id)

        else:
            
            return HttpResponse(f"INVALID FORM,\n{new_form.errors}")

    
    else:
        clean_form = CustomerRegistrationForm()
        print("Testing:",request.session["store_id"])

        return render(request,"register_customer.html",{'form':clean_form})


def register_employee(request):
    if request.method == "POST":
        new_form = EmployeeRegistrationForm(request.POST)
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
                
            account_type = new_form.cleaned_data["account_type"]

            if User.objects.filter(username=username).exists():
                return render(request,"register_employee.html",{"error_message":"Username already taken", "form":new_form})
                #raise forms.ValidationError("This username is already in use")
            
            elif  User.objects.filter(email=email_address).exists():
                return render(request,"register_employee.html",{"error_message":"Email already in use","form":new_form})
                #raise forms.ValidationError("This email is already in use")
            
            else:
                user = User(username=username,
                            password=make_password(password), 
                            email=email_address)
                user.save()

                #TODO add verification to create an employee account
                if account_type == "employee":
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
                elif account_type == "manager":
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
                elif account_type == "admin":
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
        clean_form = EmployeeRegistrationForm()
    
        return render(request,"register_employee.html",{'form':clean_form})
