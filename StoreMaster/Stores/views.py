from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from Accounts.forms import CustomerRegistrationForm,EmployeeRegistrationForm, StoreRegistrationManagerForm

from .models import *
from Accounts.models import *
from Products.models import *
from Shipments.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse("Stores Home")

def add_product_to_purchase(request,store_id,product_id,quantity):
    product = Product.objects.get(product_id=product_id)
    if "products_in_purchase" in request.session:
        print(type(product_id))
        products_in_purchase = request.session["products_in_purchase"]
        key = str(product_id)
        
        if str(product_id) in request.session.get("products_in_purchase"):
            
            current_quantity = request.session.get("products_in_purchase").get(str(product_id))[1]
            new_quantity = current_quantity + quantity
            request.session["products_in_purchase"][str(product_id)][1] = new_quantity

        else:
            request.session["products_in_purchase"][product_id] = [product.product_name,quantity]

    else:
        request.session["products_in_purchase"] = {product_id:(product.product_name,quantity)}

    
    request.session.save()

    return redirect("Stores:new_purchase",store_id)

def remove_product_from_purchase(request,store_id,product_id):
    del request.session[product_id]
    return redirect("Stores:new_purchase",store_id)

def employee_view_purchase(request,purchase_id):
    purchase_object = Purchase.objects.get(purchase_id=purchase_id)
    products_in_purchase = [obj for obj in ProductInPurchase.objects.filter(purchase_info_object=purchase_object)]

    if purchase_object.customer_id:
        name = purchase_object.customer_id.first_name + " " + purchase_object.customer_id.last_name
    else:
        name = purchase_object.first_name + " " + purchase_object.last_name

    context = {"purchase_object":purchase_object, "products_in_purchase":products_in_purchase,"name":name}

    return render(request,"employee_view_purchase.html",context=context)


def finalize_purchase(request,store_id,customer_id = None, first_name=None,last_name=None):

    account_type = request.user.userinfo.account_type
    user_id = request.user.userinfo.user_id
    employee_id = None
    manager_id=None
    admin_id=None
    if customer_id is not None:
        customer = CustomerInfo.objects.get(user_id=customer_id)

    store = Store.objects.get(store_id=store_id)
    if account_type == "employee":
        employee_id = EmployeeInfo.objects.get(user_id=user_id)

    elif account_type == "manager":
        manager_id = ManagerInfo.objects.get(user_id=user_id)
        
    elif account_type == "admin":
        admin_id = AdminInfo.objects.get(user_id=user_id)

    total = 0
    for product in request.session.get("products_in_purchase"):
        product_object = Product.objects.get(product_id=product)
        total += (product_object.product_price * request.session.get("products_in_purchase").get(product)[1])
        
    new_purchase = Purchase(store=store,employee_id=employee_id,manager_id=manager_id,admin_id=admin_id,
                            customer_id=customer,first_name=first_name,last_name=last_name,
                            purchase_date = datetime.now().date(),purchase_total=total)
    new_purchase.save()

    #TODO make sure stock gets updated, also verify that stock can handle the purchase(AKA error handling)

    #loop through items and create items in purchase
    for product in request.session.get("products_in_purchase"):
        product_object = Product.objects.get(product_id=product)
        quantity = request.session.get("products_in_purchase").get(product)[1]
        new_product_in_purchase = ProductInPurchase(purchase_info_object=new_purchase,product=product_object,quantity=quantity)
        new_product_in_purchase.save()

    del request.session["products_in_purchase"]

    return redirect("Stores:employee_view_purchase",new_purchase.purchase_id)

def new_purchase(request,store_id):
    
    if "products_in_purchase" in request.session:
        print("TESTING")
        print(request.session["products_in_purchase"])
    context = {"store_id":store_id}
    store = Store.objects.get(store_id=store_id)
    if request.method == 'POST':
        if 'product_search' in request.POST:
            search_text = request.POST.get('product_search')
            search_terms = search_text.split()
            query = Q(store_id=store_id)
            for term in search_terms:
                if term.isdigit():
                    query &= Q(product_id=term, store=store)
                else:
                    query &= (Q(product_name__icontains=term) | Q(product_description__icontains=term))
            
            products = Product.objects.filter(query)
        elif "customer_selector" in request.POST:
            customer_id = request.POST.get("customer_selector")
            print(customer_id)
            

            return finalize_purchase(request,store_id,customer_id)

            
            
        elif "new_customer_form" in request.POST:
            new_customer_form = CustomerRegistrationForm(request.POST)
            if new_customer_form.is_valid():
                new_customer_form.save()
                
                #may need new user as well
                return finalize_purchase(request,store_id,customer_id)

            else:
                #TODO error in registering a new customer to the store
                pass
        
    
    else:
        products = Product.objects.filter(store=Store.objects.get(store_id=store_id))
        context["customer_options"] = get_all_customers(store_id)
        context["new_customer_form"] = CustomerRegistrationForm()

    # if "products_in_purchase" in request.session:
    #     context["products_in_purchase"] = []
    #     for item,value in request.session["products_in_purchase"]:
    #         context["products_in_purchase"].append(value)
    context["products"] = products
    context["store_id"] = store_id
    return render(request,"new_purchase.html",context=context)

def store_home(request, store_id):
    request.session["store_id"] = store_id
    if request.user.is_authenticated:
        if request.user.userinfo.account_type == "customer":
            user = request.user

            #NEEDS TO LOAD PRODUCTS AND SUCH
        else:
            if request.user.userinfo.store:
                return redirect("Stores:manage_store",store_id=request.user.userinfo.store.store_id)
            else:
                #TODO return HttpResponse("Error: No store associated with this user")
                pass
            
    store = Store.objects.get(store_id=store_id)
    if request.method == 'POST':
        #Get search results
        print(request.POST)
        search_text = request.POST.get('search-bar')
        if search_text:
            query = Q()
            search_terms = search_text.split()
            for term in search_terms:
                query |= Q(product_name__icontains=term) | Q(product_description__icontains=term)

            products = Product.objects.filter(query,store_id=store_id)
            
        else:
            return redirect("Stores:store_home",store_id)
        
    else:
        #Get all products
        products = Product.objects.filter(store = store)
    return render(request,"store_front.html",context={"store":store,"products":products})


def view_customer_cart(request,user_id):
    context = {}
    if "cart_errors" in request.session:
        context["errors"] = request.session["cart_errors"]
        del request.session["cart_errors"]

    products_in_cart = ProductInCart.objects.filter(customer_id=user_id)
    context["products_in_cart"] = products_in_cart
    context["user_id"] = user_id
    return render(request,"view_customer_cart.html",context=context)
    return HttpResponse("CART TIMEEE")

def edit_customer_cart(request,user_id):
    products_in_cart = ProductInCart.objects.filter(customer_id=user_id)
    print(products_in_cart)
    print(request.POST)
    errors = []
    for product in products_in_cart:
        new_quantity = int(request.POST.get(f'quantity_{product.product.product_id}'))
        if new_quantity == 0:
            product.delete()
        elif new_quantity <= product.product.product_stock:
            product.quantity = new_quantity
            product.save()
        else:
            errors.append(f"{product.product.product_name} does not have enough stock for that.")

    request.session["cart_errors"] = errors
    return redirect("Stores:view_customer_cart",user_id)

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


@login_required(login_url='/login_employee')
def manage_store(request,store_id):
    store = Store.objects.get(store_id=store_id)
    products = Product.objects.filter(store=store)
    orders = Order.objects.filter(store=store)
    purchases = Purchase.objects.filter(store=store)
    customers = CustomerInfo.objects.filter(store=store)
    employees = EmployeeInfo.objects.filter(store=store)
    managers = ManagerInfo.objects.filter(store=store)
    
    employees = list(employees) + list(managers)

    if request.method == 'POST':
        if 'product_search' in request.POST:
            search_text = request.POST.get('product_search')
            search_terms = search_text.split()
            query = Q(store_id=store_id)
            for term in search_terms:
                query &= (Q(product_name__icontains=term) | Q(product_description__icontains=term))

            products = Product.objects.filter(query)

        elif 'order_search' in request.POST:
            #TODO could add searhcing for user as well.
            search_text = request.POST.get("order_search")
            search_terms = search_text.split()
            query = Q(store=store)
            for term in search_terms:
                if term.isdigit():
                    query &= (Q(order_id__icontains=int(term)))
            
            orders = Order.objects.filter(query)

        elif 'purchase-search-form' in request.POST:
            #TODO could add searhcing for user as well.
            search_text = request.POST.get("purchase_search")
            search_terms = search_text.split()
            query = Q(store=store)
            for term in search_terms:
                if term.isdigit():
                    query &= (Q(purchase_id__icontains=int(term)))
            
            purchases = Purchase.objects.filter(query)
        elif 'customer-search-form' in request.POST:
            pass
        elif 'employee-search-form' in request.POST:
            pass
        
    else:

        context = {}
        userinfo = request.user.userinfo
        if Store.objects.filter(store_id = store_id).exists():

            request.session["store_id"] = store_id
            context["account_type"] = userinfo.account_type
            context["Store name"] = Store.objects.get(store_id=store_id).store_name
            context["user"] = request.user
            
        else:
            return HttpResponse("Sorry, no stores found with that ID.")
            #Could put a seperate search page for finding a store.


    shipments = Shipment.objects.filter(destination_store=store_id)

    context = { "products":products,
                "orders":orders,
                "purchases":purchases,
                "customers":customers,
                "employees":employees,
                "shipments":shipments }
    
    return render(request,"manage_store.html",context)

def admin_manage_stores(request):
    if request.method == 'POST':
        print(dict(request.POST))
        if 'store_selector' in request.POST:
            return redirect("Stores:manage_store",store_id=request.POST.get('store_selector'))
        elif 'employee_selector' in request.POST:
            return redirect('Accounts:view_user',user_id=request.POST.get('employee_selector'))
        elif 'customer_selector' in request.POST:
            return redirect('Accounts:view_user',user_id=request.POST.get('customer_selector'))
    
    else:
        stores = []
        for store in Store.objects.all():
            stores.append((store.store_id,str(store)))

        employees = []
        for manager in ManagerInfo.objects.all():
            print(manager)
            employees.append((manager.user_id,str(manager)))
        for employee in EmployeeInfo.objects.all():
            print(employee)
            employees.append((employee.user_id,str(employee)))
        for admin in AdminInfo.objects.all():
            print(admin)
            employees.append((admin.user_id,str(admin)))
        
        customers = []
        for customer in CustomerInfo.objects.all():
            customers.append((customer.user_id,str(customer)))

        context = {"stores":stores,
                "employees":employees,
                "customers":customers}
        
                                                                                        
        return render(request, "admin_manage_stores.html",context)
        return HttpResponse("admin timeeee")

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


def search_for_store(request):
    if request.method == 'POST':
        context = {}
        search_contents = request.POST.get('store_search_bar')
        #TODO could add address searching
        if search_contents.isdigit():
            if Store.objects.filter(store_id=int(search_contents)).exists():
                context["results"] = Store.objects.filter(store_id=int(search_contents))

            else:
                context["no_results"] = "Sorry, no stores were found with that ID"
        else:
            search_words = search_contents.split()
            result = Q()
            for word in search_words:
                result |= Q(store_name__icontains=word)
            
            search_results = Store.objects.filter(result)
            if search_results:
                
                context["results"] = search_results
            else:
                context["no_results"] = "Sorry, no stores found"

        return render(request,"home.html",context)

def get_all_customers(store_id):
    customers = []
    for customer in CustomerInfo.objects.filter(store=Store.objects.get(store_id=store_id)):
        customers.append((customer.user_id,str(customer)))

    return customers

def get_all_managers():
    #Get all existing managers to use in manager selector
    managers= []
    for manager in ManagerInfo.objects.all():
        managers.append((manager.user_id,str(manager)))

    return managers

def register_store_page_1(request):
    if "store_info" in request.session:
        form = StoreRegistrationForm(request.session["store_info"])
        store_info = request.session["store_info"]
        del request.session["store_info"]
    else:
        form = StoreRegistrationForm()

    manager_info = None
    manager_id = None
    if "manager_info" in request.session:
        manager_info = request.session["manager_info"]
        del request.session["manager_info"]

    elif "manager_id" in request.session:
        manager_id = request.session["manager_id"]
        del request.session["manager_id"]

    if request.method == "POST":
        filled_out_registration_form = StoreRegistrationForm(request.POST)
        if filled_out_registration_form.is_valid():
            request.session["store_info"] = filled_out_registration_form.cleaned_data

            

            return redirect("Stores:register_store_page_2")
            #return render(request,"register_store_page_2.html",context={"store_info":request.POST})
        else:
            #Add any error messages up top
            return render(request,"register_store_page_1.html",{'form':form,'error':'A store with that name exists at that location already'})
        
    else:
        if manager_info is not None:
            request.session["manager_info"] = manager_info
        elif manager_id is not None:
            request.session["manager_id"] = manager_id
        
        return render(request, "register_store_page_1.html", {'form': form})

def register_store_page_2(request,error = None):
    #Grab store info 
    print(dict(request.session))

    manager_info = None
    manager_id = None

    store_info = request.session["store_info"]
    del request.session["store_info"]

    form = None
    
    #Create user registration form for a new manager to be registered
    if "manager_info" in request.session:
        manager_info = request.session["manager_info"]
        form = StoreRegistrationManagerForm(manager_info)
        del request.session["manager_info"]

        
    elif "manager_id" in request.session:
        manager_id = request.session["manager_id"]
        del request.session["manager_id"]

    if form is None:
        form = StoreRegistrationManagerForm()
    

    if request.method == "POST":
        context = {}
        request.session["store_info"] = store_info
        # context = {"store":store_info}
        #If the user is using a pre existing manager
        if request.POST.get('form_type') == "register_existing":
            manager = ManagerInfo.objects.get(user_id = request.POST.get("manager_selector"))
            request.session["manager_id"] = manager.user_id
            if manager.store:  #If the manager is alread assigned to a store
                manager_options = get_all_managers()
                return render(request,"register_store_page_2.html",{'form':form, 'manager_options':manager_options,'error':f'{manager.first_name} {manager.last_name} is already assigned to a store'})
            else:
                manager_id = manager.user_id 
            

            context["load_new_manager_first"] = False
            context["manager"] = manager #Passing the manager object itself to the template
            return render(request,"register_store_page_3.html",context=context)
        
        #If the user is registering a new manager to ues for this store
        if request.POST.get('form_type') == "register_new":            
            filled_out_manager_form = StoreRegistrationManagerForm(request.POST)
            print(request.POST)
            if filled_out_manager_form.is_valid():
                manager_data = filled_out_manager_form.cleaned_data
                # del manager_data["user_type"]
                manager_data['birthday'] = manager_data["birthday"].strftime('%Y-%m-%d') #Converting to string for data transfer to request session
                request.session["manager_info"] = manager_data
                context["manager"] = filled_out_manager_form.cleaned_data

                
                context["load_new_manager_first"] = True
                return render(request,"register_store_page_3.html",context=context)
            
            #Error in manager registration form
            else:
                print(filled_out_manager_form.errors)
                manager_data = filled_out_manager_form.cleaned_data
                form_errors = filled_out_manager_form.errors
                if "__all__" in form_errors:
                    context["error"] = form_errors["__all__"]

                    error = str(context["error"])
                    if "username" in error:
                        manager_data["username"] = ""
                    
                    if "email address" in error:
                        manager_data["email_address"] = ""

                context["form"] = EmployeeRegistrationForm(manager_data)
                context["load_new_manager_first"] = True
                
                return render(request,"register_store_page_2.html",context=context)

    else:
        manager_options = get_all_managers()
        context = {"manager_options":manager_options, "form":form}

        if manager_info is not None:
            request.session["manager_info"] = manager_info
            context["load_new_manager_first"] = True

        elif manager_id is not None:
            request.session["manager_id"] = manager_id

            context["selected_manager_name"] = str(ManagerInfo.objects.get(user_id=manager_id))
            context["selected_manager_id"] = manager_id 

            context["load_new_manager_first"] = False
        
        request.session["store_info"] = store_info

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
    
    #Preexisting manager
    try:
        manager_id = request.session["manager_id"]
        new_manager = ManagerInfo.objects.get(user_id=manager_id)

    #New manager
    except KeyError:
        manager_data = request.session["manager_info"]
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

    del request.session["store_info"]
    if "manager_id" in request.session:
        del request.session["manager_id"]
    elif "manager_info" in request.session:
        del request.session["manager_info"]

    return HttpResponse("HI")

def view_shipment(request,shipment_id):
    print(shipment_id)
    pass
def view_all_shipments(request,store_id):
    pass



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
#                     return HttpResponse("OK I DON'T KNOW WHAT'S GOING ON")fds 
#                 # except ValidationError:
#                 #     return HttpResponse("nope, error in the user form")

#                 return HttpResponse("ok, a new manager")
#         else:
#             return render(request,"DELETE_ME_ERROR_VIEW.html",context={"form":filled_out_registration_form})
#             return HttpResponse("OK WHAT")
#     else:
#         empty_form = StoreRegistrationForm()
#         return render(request, "register_store.html", {'form': empty_form})
