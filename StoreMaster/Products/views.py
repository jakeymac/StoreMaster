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

def product_view(request, store_id, product_id):
    store = Store.objects.get(store_id=store_id)
    product = Product.objects.get(product_id=product_id,store=store)
    context = {"product":product}
                
    return render(request,"product_view.html",context)

def product_edit_view(request,store_id,product_id):
    store = Store.objects.get(store_id=store_id)
    product = Product.objects.get(product_id=product_id,store=store)
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
            
        return redirect('Products:product_view',store_id=store_id,product_id=product_id)
    else:
        print("Not POST step 2")
        product_form = EditProductForm(instance=product)
        return render(request, "edit_product.html",{'form':product_form,'product_id':product_id,'store_id':store_id})