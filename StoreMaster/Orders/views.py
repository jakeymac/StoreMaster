from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order
from Products.models import ProductInOrder

# Create your views here.
def index(request):
    return HttpResponse("Orders Home")

def view_order(request,order_id):
    order = Order.objects.get(order_id=order_id)
    products = ProductInOrder.objects.filter(order_info_object=order)

    context = {"order":order, "products":products}

    return render(request,"view_customer_order.html",context=context)

def view_customer_orders(request,user_id):
    orders = [order for order in Order.objects.filter(customer_id=user_id)]
    context = {"orders":orders}
    return render(request,"view_customer_orders.html",context=context)
