from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

from Accounts.models import *
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from Accounts.forms import UserRegistrationForm


from datetime import datetime
# Create your views here.
def index(request):
    return HttpResponse("Stores Home")

@login_required(login_url='/login')
def manage_store(request,store_name):
    context = {}
    userinfo = request.user.userinfo
    #Check if logged in user is a customer, not a staff member or admin
    if hasattr(userinfo,"customerinfo"):
        #SEND TO THE CUSTOMER VIEW
        return HttpResponse("CUSTOMER INFO ")

    elif hasattr(userinfo,"admininfo"):
        context["user_type"] = "admin"

    elif hasattr(userinfo, 'managerinfo'):
        if userinfo.managerinfo.store.store_name != store_name:
            context["correct_store_name":userinfo.managerinfo.store.store_name]

        context["user_type"] = "manager"

    elif hasattr(userinfo,"employeeinfo"):
        if userinfo.employeeinfo.store.store_name != store_name:
            context["correct_store_name":userinfo.employeeinfo.store.store_name]

        context["user_type"]="employee"



    return render(request,"manage_store.html",context=context)


def get_all_managers():
    #Get all existing managers to use in manager selector
    managers= []
    for manager in ManagerInfo.objects.all():
        managers.append((manager.user_id,str(manager)))

    return managers

def register_store_page_1(request):
    empty_form = StoreRegistrationForm()
    if request.method == "POST":
        filled_out_registration_form = StoreRegistrationForm(request.POST)
        if filled_out_registration_form.is_valid():
            request.session["store_info"] = filled_out_registration_form.cleaned_data
            return redirect("Stores:register_store_page_2")
            #return render(request,"register_store_page_2.html",context={"store_info":request.POST})
        else:
            #Add any error messages up top
            return render(request,"register_store_page_1.html",{'form':empty_form,'error':'A store with that name exists at that location already'})
        
    else:
        return render(request, "register_store_page_1.html", {'form': empty_form})

def register_store_page_2(request,error = None):
    #Create user registration form for a new manager to be registered
    clean_user_form = UserRegistrationForm()

    if request.method == "POST":
        context = {"store":request.session["store_info"]}
        #If the user is using a pre existing manager
        if request.POST.get('form_type') == "register_existing":
            manager = ManagerInfo.objects.get(user_id = request.POST.get("manager_selector"))
            if manager.store:  #If the 
                manager_options = get_all_managers()
                return render(request,"register_store_page_2.html",{'form':clean_user_form, 'manager_options':manager_options,'error':f'{manager.first_name} {manager.last_name} is already assigned to a store'})
            else:
                manager_id = manager.user_id
                request.session["manager_id"] = manager_id #Passing along manager ID to pull the manager later
            context["manager"] = manager #Passing the manager object itself to the template
            return render(request,"register_store_page_3.html",context=context)
        
        #If the user is registering a new manager to ues for this store
        if request.POST.get('form_type') == "register_new":
            filled_out_manager_form = UserRegistrationForm(request.POST)
            
            if filled_out_manager_form.is_valid():
                manager_data = filled_out_manager_form.cleaned_data
                del manager_data["user_type"]
                manager_data['birthday'] = manager_data["birthday"].strftime('%Y-%m-%d') #Converting to string for data transfer to request session
                request.session["manager_dict"] = manager_data
                context["manager"] = filled_out_manager_form.cleaned_data

                return render(request,"register_store_page_3.html",context=context)
            
            #Error in manager registration form
            else:
                manager_data = filled_out_manager_form.cleaned_data
                form_errors = filled_out_manager_form.errors
                if "__all__" in form_errors:
                    context["error"] = form_errors["__all__"]

                    error = str(context["error"])
                    if "username" in error:
                        manager_data["username"] = ""
                    
                    if "email address" in error:
                        manager_data["email_address"] = ""

                context["form"] = UserRegistrationForm(manager_data)
                context["load_new_manager_first"] = True
                
                return render(request,"register_store_page_2.html",context=context)

    else:
        manager_options = get_all_managers()
        context = {"manager_options":manager_options, "form":clean_user_form}
        if error:
            context["error"] = error
        return render(request,"register_store_page_2.html",context=context)
    

def edit_current_registration(request):
    pass
    
#Final Confirmation
def confirm_store_registration(request):
    
    store_info = request.session["store_info"]

    #convert key names to remove "store_"
    converted_store_info = {}
    for key, value in store_info.items():
        if key == "store_name":
            converted_store_info[key] = value

        elif key == "store_state":
            converted_store_info["state"] = value

        else:
            converted_store_info[key.lstrip("store_")] = value

    new_store = Store(**converted_store_info)
    new_store.save()
    
    try:
        manager_id = request.session["manager_id"]
        new_manager = ManagerInfo.objects.get(user_id=manager_id)

    except KeyError:
        manager_data = request.session["manager_dict"]
        birthday_string = manager_data["birthday"]
        birthday_date = datetime.strptime(birthday_string, "%Y-%m-%d")
        manager_data["birthday"] = birthday_date

        
        
        new_user = User(username=manager_data["username"],
                        password=make_password(manager_data["password"]),
                        email=manager_data["email_address"])
        
        new_user.save()
        new_manager = ManagerInfo(**manager_data)
        new_manager.user = new_user

    new_manager.store = new_store

    new_manager.save()
    return HttpResponse("HI")


#TODO delete this function, not being used: 

# def register_store(request):
#     if request.method == "POST":
#         filled_out_registration_form = StoreRegistrationForm(request.POST)
#         if filled_out_registration_form.is_valid():
#             #Check if the user has decied to use a pre-existing manager for this store or not3
#             manager_type_choice = request.POST.get("manager_type_choice")
#             if manager_type_choice == "new":
#             if manager_type_choice == "pre-existing":
#                 return HttpResponse("ok, pre-existing")
#             else:
#                 #Try to crete a new manager
#                 # try:
#                 print("Creating new manager now")
#                 new_manager_info = {
#                     "first_name":filled_out_registration_form.cleaned_data["manager_first_name"],
#                     "last_name":filled_out_registration_form.cleaned_data["manager_last_name"],
#                     "email_address":filled_out_registration_form.cleaned_data["manager_email_address"],
#                     "address":filled_out_registration_form.cleaned_data["manager_address"],
#                     "line_two":filled_out_registration_form.cleaned_data["manager_line_two"],
#                     "city":filled_out_registration_form.cleaned_data["manager_city"],
#                     "state":filled_out_registration_form.cleaned_data["manager_state"],
#                     "zip":filled_out_registration_form.cleaned_data["manager_zip"],
#                     "username":filled_out_registration_form.cleaned_data["manager_username"],
#                     "password":filled_out_registration_form.cleaned_data["manager_password"],
#                     "other_information":filled_out_registration_form.cleaned_data["manager_other_information"],
#                     "birthday":filled_out_registration_form.cleaned_data["manager_birthday"],
#                     "user_type":"manager"
#                 }
#                 print("New manager info done")
#                 new_user_form = UserRegistrationForm(initial=new_manager_info)
#                 print("new user form has been created")
#                 if new_user_form.is_valid():
#                     print("Let's validate")
#                     return HttpResponse("OK THE USER FORM IS VALID")
#                 else:
#                     print("it didn't vlaidate")
#                     return render(request,"DELETE_ME_ERROR_VIEW.html",context={"form":filled_out_registration_form})
#                     return HttpResponse("OK I DON'T KNOW WHAT'S GOING ON")
#                 # except ValidationError:
#                 #     return HttpResponse("nope, error in the user form")

#                 return HttpResponse("ok, a new manager")
#         else:
#             return render(request,"DELETE_ME_ERROR_VIEW.html",context={"form":filled_out_registration_form})
#             return HttpResponse("OK WHAT")
#     else:
#         empty_form = StoreRegistrationForm()
#         return render(request, "register_store.html", {'form': empty_form})
