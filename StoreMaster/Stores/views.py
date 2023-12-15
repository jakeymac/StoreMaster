from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from Accounts.forms import CustomerRegistrationForm,EmployeeRegistrationForm, StoreRegistrationManagerForm

from .models import *
from Accounts.models import *
from Products.models import *
from Shipments.models import *
from Shipments.forms import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import model_to_dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from datetime import datetime

import json


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

def confirm_new_order(request,customer_id):
    #TODO check to make sure no fields are empty
        total = 0 
        customer = CustomerInfo.objects.get(user_id=customer_id)
        products_in_cart = ProductInCart.objects.filter(customer_id=customer)
        for product_in_cart in products_in_cart:
            product = product_in_cart.product
            
            if product.product_stock < product_in_cart.quantity:
                #TODO error here for not enough stock
                return redirect("Stores:view_customer_cart",customer_id)
            
            if request.method == "POST":
                total += product_in_cart.quantity * product.product_price


        if request.method == "POST":
            address = request.POST.get("address")
            line_two = request.POST.get("line_two")
            city = request.POST.get("city")
            state = request.POST.get("state")
            zip = request.POST.get("zip")

            date = datetime.now()
            customer = CustomerInfo.objects.get(user_id=customer_id)
            store = Store.objects.get(store_id=customer.store_id)

            new_order = Order(store=store,
                              customer_id=customer,
                              order_date=date,
                              order_total=total,
                              shipping_address=address,
                              shipping_line_two=line_two,
                              shipping_city=city,
                              shipping_state=state,
                              shipping_zip=zip)
            
            new_order.save()
            for product_in_cart in products_in_cart:
                new_product_in_order = ProductInOrder(order_info_object=new_order,
                                                      product=product_in_cart.product,
                                                      quantity=product_in_cart.quantity)
                
                new_product_in_order.save()
                product_in_cart.product.update_stock(-product_in_cart.quantity)

            del request.session["products_in_cart"]
            return redirect("Stores:view_order",new_order.order_id)

                   
        
        return render(request,"confirm_order.html",{"customer":customer})



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
    context = {}
    #TODO ADD messages support instead of context, to re redner the new_purchase page. Use redirect instead of render. 
    # Use the messages framework to render the out of stock items in the html doc
    for product in request.session.get("products_in_purchase"):
        product_object = Product.objects.get(product_id=product)
        quantity = request.session.get("products_in_purchase").get(product)[1]
        if product_object.product_stock < quantity:
            if "not_enough_stock" in context:
                context["not_enough_stock"].append(product_object.product_name)
            else:
                context["not_enough_stock"] = [product_object.product_name]

            print("NOT ENOUGH STOCKKKKK")
        total += (product_object.product_price * quantity)


    if "not_enough_stock" in context:
        return redirect("Stores:new_purchase",store_id=store_id)

        return render(request,"new_purchase.html",context=context)
    
    new_purchase = Purchase(store=store,employee_id=employee_id,manager_id=manager_id,admin_id=admin_id,
                            customer_id=customer,first_name=first_name,last_name=last_name,
                            purchase_date = datetime.now().date(),purchase_total=total)
    new_purchase.save()

    #TODO make sure stock gets updated, also verify that stock can handle the purchase(AKA error handling)

    #loop through items and create items in purchase
    for product in request.session.get("products_in_purchase"):
        product_object = Product.objects.get(product_id=product)
        
        quantity = request.session.get("products_in_purchase").get(product)[1]
        product_object.update_stock(-quantity)
        #TODO STOCK IS BEING CHANGED HERE
        
        new_product_in_purchase = ProductInPurchase(purchase_info_object=new_purchase,product=product_object,quantity=quantity)
        new_product_in_purchase.save()

    del request.session["products_in_purchase"]

    return redirect("Stores:employee_view_purchase",new_purchase.purchase_id)

def new_purchase(request,store_id):
    context = {}
    products = []
    context["products"] = products
    if "products_in_purchase" in request.session:
        print("TESTING")
        print(request.session["products_in_purchase"])
    context = {"store_id":store_id}
    store = Store.objects.get(store_id=store_id)
    if request.method == 'POST':
        if 'product_search' in request.POST:
            print(product_search)
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
            print("existing")
            customer_id = request.POST.get("customer_selector")
            print(customer_id)
            

            return finalize_purchase(request,store_id=store_id,customer_id=customer_id)

            
            
        elif "new_indicator" in request.POST:
            new_customer_form = CustomerRegistrationForm(request.POST)
            print(new_customer_form.errors)
            if new_customer_form.is_valid():
                print("hi")
                data = new_customer_form.cleaned_data
                user = User.objects.create(username=data["username"],
                                           password=data["password"],
                                           email=data["email_address"])
                
                
                new_customer = CustomerInfo.objects.create(**new_customer_form.cleaned_data,user=user,store=Store.objects.get(store_id=store_id))
                # new_customer.store = Store.objects.get(store_id=store_id)
                # new_customer.user = user
                new_customer.save()
                user.save()
                customer_id = new_customer.user_id
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

            sort_choice = request.POST.get("sort-selector")
            
            if sort_choice:
                if sort_choice == "alphabetical_descend":
                    products = Product.objects.filter(query,store_id=store_id).order_by("product_name")
                elif sort_choice == "alphabetical_ascend":
                    products = Product.objects.filter(query,store_id=store_id).order_by("-product_name")
                elif sort_choice == "price-low-to-high":
                    products = Product.objects.filter(query,store_id=store_id).order_by("product_price")
                elif sort_choice == "price-high-to-low":
                    print("sorting")
                    products = Product.objects.filter(query,store_id=store_id).order_by("-product_price")
            
            print(products)
                
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

def stock_product_from_shipment(request,shipment_id,product_id,render_page=True):
    product = Product.objects.get(product_id=product_id)
    product_in_shipment_object = ProductInShipment.objects.get(shipment_id=shipment_id,product=product)
    product.update_stock(product_in_shipment_object.quantity)
    product_in_shipment_object.status = "stocked"
    product_in_shipment_object.save()

    shipment = Shipment.objects.get(shipment_id=shipment_id)
    shipment.status = "stocking in progress"
    shipment.save()
    if render_page: #Used if stocking all products.
        return redirect("Stores:view_shipment", shipment_id)

def stock_all_products_from_shipment(request, shipment_id):

    shipment = Shipment.objects.get(shipment_id=shipment_id)
    product_in_shipment_objects = ProductInShipment.objects.filter(shipment=shipment)
    for product in product_in_shipment_objects:
        if product.status == "not stocked":
            stock_product_from_shipment(request,shipment_id,product.product.product_id,render_page=False)
            product.status = "stocked"
            product.save()

    shipment.shipment_status = "closed"
    shipment.save()
    
    return redirect("Stores:view_shipment", shipment_id)

def add_item_to_shipment(request,product_id,quantity):
    product = Product.objects.get(product_id=product_id)
    if "items_in_shipment" in request.session:
        if product_id in request.session["items_in_shipment"]:
            request.session.get(product_id)[1] += quantity
        else:
            request.session["items_in_shipment"][product_id] = [product.product_name,quantity]
    else:
        request.session["items_in_shipment"] = {product_id:[product.product_name,quantity]}

    
    return redirect("add_new_shipment",product.store.store_id)


def add_new_shipment(request,store_id):
    store = Store.objects.get(store_id=store_id)
    if request.method == "POST":
        #Add new item to the shipment
        if "quantity_selector" in request.POST:
            product_id = request.POST.get("product_id")
            quantity = request.POST.get('quantity_selector')

            return add_item_to_shipment(request,product_id,quantity)
        
        #Import shipment and items details from an uploaded file
        elif "json_file" in request.POST:
            form = ShipmentJSONFileForm(request.POST,request.FILES)
            if form.is_valid():
                json_file = form.cleaned_data['json_file']

                try:
                    json_data = json.load(json_file)
                    try:
                        shipment_origin = json_data.get("shipment_origin")
                        destination_store = Store.objects.get(product_id=json_data.get("destination_store_id"))
                        shipped_date = json_data.get("shipped_date")
                        expected_date = json_data.get("expected_date")
                        shipment_tracking_num = json_data.get("tracking_number")
                        shipment_freight_company =  json_data.get("shipping_company")

                        new_shipment = Shipment(shipment_origin=shipment_origin,
                                                destination_store=destination_store,
                                                shipped_date=shipped_date,
                                                expected_date=expected_date,
                                                shipment_tracking_num=shipment_tracking_num,
                                                shipment_freight_company=shipment_freight_company)
                        
                        new_shipment.save()
                       
                        for product in json_data.get("products"):
                            shipment_id = new_shipment.shipment_id
                            product = Product.objects.get(product_id=product.get("product_id"))
                            quantity = product.get("quantity")
                            
                            new_product_in_shipment = ProductInShipment(shipment_id=shipment_id,
                                                                        product=product,
                                                                        quantity=quantity,
                                                                        status="not stocked")
                            
                            new_product_in_shipment.save()



                    except KeyError:
                        pass
                except json.JSONDecodeError as e : 
                    error_message = f"Error parsing JSOn file: {e}"

                return redirect("view_shipment",new_shipment.shipment_id)
            else:
                #TODO error cehcking here for error in json form
                pass


        #Finalizing new shipment with details and items
        elif "shipped_date" in request.POST:
            form = NewShipmentForm(request.POST,store=store)
            if form.is_valid():
                new_shipment = form.save()
                shipment_id = new_shipment.shipment_id

                for product in request.session["items_in_shipment"]:
                    current_product = Product.objects.get(product_id=product)
                    quantity = request.session["items_in_shipment"].get(product)[1]
                    new_product_in_shipment = ProductInShipment(shipment=new_shipment,
                                                                product=current_product,
                                                                quantity = quantity,
                                                                status="not stocked")
                    
                    new_product_in_shipment.save()

                return redirect("view_shipment",shipment_id)

            
    else:
        #if json_data is not None:
            #pass
        #else:
            clean_form = NewShipmentForm()
            json_form = ShipmentJSONFileForm()
            return render(request,"add_new_shipment.html",context={"form":clean_form,"json_form":json_form}) 

def view_shipment(request,shipment_id):
    if request.method == "POST":
        if "shipment_status_selector" in request.POST:
            new_status = request.POST.get("shipment_status_selector")
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            shipment.shipment_status = new_status
            shipment.save()

        elif "product_status_selector" in request.POST:
            new_status = request.POST.get("product_status_selector")
            shipment = Shipment.objects.get(shipment_id=shipment_id)
            if new_status == "not stocked":
                shipment.shipment_status = "stocking in progress"
                shipment.save()

            product_id = request.POST.get("product_id")
            product = Product.objects.get(product_id=product_id)
            product_in_shipment = ProductInShipment.objects.get(product=product,shipment=shipment)
            product_in_shipment.status = new_status
            product_in_shipment.save()



    shipment = Shipment.objects.get(shipment_id=shipment_id)
    products = ProductInShipment.objects.filter(shipment=shipment)

    context = {"shipment":shipment,"products":products}
        
    return render(request,"view_shipment.html",context=context)

def view_all_shipments(request,store_id):
    store = Store.objects.get(store_id=store_id)
    shipments = Shipment.objects.filter(destination_store=store)

    context={"shipments":shipments,"store_id":store_id}
    return render(request,"view_all_shipments.html",context=context)

def get_order_information(order_id):
    order = Order.objects.get(order_id=order_id)
    products = []
    for instance in ProductInOrder.objects.filter(order_info_object=order):
        products.append(instance)

    return order, products

def view_order(request,order_id):
    order, products = get_order_information(order_id)
    context = {"order":order,"products":products,}

    return render(request,"view_order.html",context=context)

def employee_view_order(request,order_id):
    order, products = get_order_information(order_id)
    context = {"order":order,"products":products}

    return render(request,"employee_view_order.html",context=context)



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

    products_in_low_stock = []
    for product in products:
        if product.product_stock <= product.low_stock_quantity:
            products_in_low_stock.append(product)

    

    if request.method == 'POST':
        if 'product_search' in request.POST:
            search_text = request.POST.get('product_search')
            search_terms = search_text.split()
            query = Q(store_id=store_id)
            for term in search_terms:
                if term.isdigit():
                    query &= Q(product_id=term)

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
                
                query &= (Q(customer_id__first_name__icontains=term) | Q(customer_id__last_name__icontains=term))
            
            orders = Order.objects.filter(query)

        elif 'purchase_search' in request.POST:
            #TODO could add searhcing for user as well.
            search_text = request.POST.get("purchase_search")
            search_terms = search_text.split()
            query = Q(store=store)
            for term in search_terms:
                if term.isdigit():
                    query &= (Q(purchase_id__icontains=int(term)))
                
                query &= (Q(customer_id__first_name__icontains=term) | Q(customer_id__last_name__icontains=term))
            
            purchases = Purchase.objects.filter(query)
        elif 'customer_search' in request.POST:
            search_text = request.POST.get("customer_search")
            search_terms = search_text.split()
            query = Q(store=store)
            for term in search_terms:
                if term.isdigit():
                    query &= (Q(user_id=term))
                #Users' names and last names aren't going to have numbers
                else:
                    query &= (Q(first_name__icontains=term) | Q(last_name__icontains=term))

            customers = CustomerInfo.objects.filter(query)
            
        elif 'employee_search' in request.POST:
            search_text = request.POST.get("employee_search")
            search_terms = search_text.split()
            query = Q(store=store)
            for term in search_terms:
                if term.isdigit():
                    query &= (Q(user_id=term))
                else:
                    query &= (Q(first_name__icontains=term) | Q(last_name__icontains=term))

            employees = EmployeeInfo.objects.filter(query)
            managers = ManagerInfo.objects.filter(query)

            employees = list(employees) + list(managers)

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


        #TODO maybe delete this, not sure what it's doing here.
        context = {}
        userinfo = request.user.userinfo
        if Store.objects.filter(store_id = store_id).exists():
            pass

    shipments = Shipment.objects.filter(destination_store=store_id)

    context = { "store":Store.objects.get(store_id=store_id),
                "products":products,
                "orders":orders,
                "purchases":purchases,
                "customers":customers,
                "employees":employees,
                "shipments":shipments,
                "low_stock_products":products_in_low_stock }
    
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
            context["store"] = manager.store
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

    return redirect("Stores:manage_store",new_store.store_id)



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
