from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from Products.forms import EditProductForm, NewProductForm

from Products.models import *
from Stores.models import *

# Create your views here.
def index(request):
    return HttpResponse("Products Home")

def product_view(request, store_id, product_id):
    store = Store.objects.get(store_id=store_id)
    product = Product.objects.get(product_id=product_id,store=store)

    context = {"product":product}
                
    return render(request,"product_view.html",context)

def product_edit_view(request,store_id,product_id):
    store = Store.objects.get(store_id=store_id)
    product = Product.objects.get(product_id=product_id,store=store)

    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

        return HttpResponse("Done Editing!")

    else:
        product_form = EditProductForm(instance=product)
        return render(request, "edit_product.html",{'form':product_form})


def product_registration_view(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponse("Done!")

    else:
        clean_form = NewProductForm()

    
