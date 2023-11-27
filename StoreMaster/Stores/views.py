from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from Accounts.forms import UserRegistrationForm

from .models import *
from Accounts.models import *
from Products.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse("Stores Home")


def manage_store_redirect_from_home(request):
    if request.method == 'POST':
        store_name = request.POST.get("store_name")
        store_id = request.POST.get("store_id")

        most_definite = Store.objects.filter(store_name=store_name,store_id=store_id)

        possible_by_name = Store.objects.filter(store_name=store_name)
        possible_by_id = Store.objects.filter(store_id=store_id)
        
        if most_definite:
            #Found an exact match for name and ID
            print(most_definite)
            print(most_definite[0].store_id)
            return manage_store(request,most_definite[0].store_id)

        else:
            #Go through and show results of stores with same name, and 
            #the store that matches the id provided (if it exists)
            pass

        for item in possible_by_name:
            print(item,item.store_id)
        
        for item in possible_by_id:
            print(item,item.store_name)

        print(most_definite)
        #print(possible_by_name)
        #print(possible_by_id)
        #return render(request)
        return HttpResponse("Results printed")

    else:
        return render(request,"manage_store_home.html",{"load":True})
    return HttpResponse("testing MANAGE STORE REDIRECT")


@login_required(login_url='/login')
def manage_store(request,store_id):
    context = {}
    userinfo = request.user.userinfo
    request.session["store_id"] = store_id
    context["user_type"] = userinfo.account_type
    context["Store name"] = Store.objects.get(store_id=store_id).store_name

    return render(request,"manage_store.html",context)

def product_view(request):
    pass

def view_store(request,store_name):
    #Check if a user is logged in, if they are and they're a manager, they should be forwarded to the manage_store version.
    pass

def product_search(request):
    search = request.GET["product_search"]
    if search:
        store = Store.objects.get(store_id=request.session["store_id"])
        results = Product.objects.filter(
            Q(product_name__icontains=search) | Q(product_description__icontains=search), 
            store=store
        )
        results = [result for result in results]
    else:
        results = []
    
    context = {"results":results,"search":search}
    return render(request, "product_search_results.html",context=context)


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
