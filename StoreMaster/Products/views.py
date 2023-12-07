from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from Products.forms import EditProductForm, NewProductForm

from Products.models import *
from Stores.models import *

# Create your views here.
def index(request):
    return HttpResponse("Products Home")

def add_product_view(request,store_id):
    store = Store.objects.get(store_id=store_id)
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES,initial={'store':store})
        if form.is_valid():
            new_product = form.save()
            #new_product.save()
            product_id = new_product.product_id
            return product_view(request,store_id,product_id)
        
        else:
            return HttpResponse("ERROR: THIS NEEDS A NEW PAGE MADE")
    else:
        
        cleanForm = NewProductForm(initial={'store':store_id})
        context = {"form":cleanForm}
        return render(request,"new_product.html",context)

def product_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    store = Store.objects.get(store_id=product.store_id)
    quantities = [num for num in range(1, product.product_stock + 1)]
    context = {"product":product,"quantities":quantities}
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        customer = CustomerInfo.objects.get(user=request.user)
        if quantity > Product.objects.get(product_id=product_id).product_stock:
            #TODO error here for quantity being over, say if another customer has bought items.
            pass
        if ProductInCart.objects.filter(product_id=product_id,customer_id=customer).exists():
            product_in_cart = ProductInCart.objects.get(product_id=product_id,customer_id=customer)
            if product_in_cart.quantity + quantity > Product.objects.get(product_id=product_id).product_stock:
                #TODO ERROR here for quantity being too much
                pass
            else:
                product_in_cart.quantity += quantity
                product_in_cart.save()

        else:
            new_product_in_cart = ProductInCart(customer_id = customer,
                                                product=Product.objects.get(product_id=product_id),
                                                quantity = quantity)
            
            new_product_in_cart.save()
                    
    return render(request,"product_view.html",context)

def product_edit_view(request,product_id):
    product = Product.objects.get(product_id=product_id,store=store)
    store = Store.objects.get(store_id=product.store_id)
    print("Step 1")
    
    if request.method == 'POST':
        print("Step 2")
        form = EditProductForm(request.POST,request.FILES,instance = product)
        if form.is_valid():
            print("Step 3")
            form.save()
        else:
            form_errors = form.errors
            print("Step 4")
            print(form_errors)
            print("\n")
            
        return redirect('Products:product_view',product_id=product_id)
    else:
        print("Not POST step 2")
        product_form = EditProductForm(instance=product)
        return render(request, "edit_product.html",{'form':product_form,'product_id':product_id,'store_id':store_id})