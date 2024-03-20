from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.core.serializers import serialize
from Products.forms import EditProductForm, NewProductForm

from Products.models import *
from Stores.models import *

from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from datetime import datetime, timedelta
import math

from collections import defaultdict

from io import BytesIO
import base64

import json

# Create your views here.
def index(request):
    return HttpResponse("Products Home")

def delete_product(request,product_id):
    product = Product.objects.get(product_id=product_id)
    store = product.store
    product.delete()
    return redirect("Stores:manage_store",store.store_id)

def add_product_view(request,store_id):
    store = Store.objects.get(store_id=store_id)
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES,initial={'store':store})
        if form.is_valid():
            new_product = form.save()
            #new_product.save()
            product_id = new_product.product_id
            return redirect("Products:employee_view_product",product_id)
        
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
    product = Product.objects.get(product_id=product_id)
    #store = Store.objects.get(store_id=product.store_id)
    
    if request.method == 'POST':
        form = EditProductForm(request.POST,request.FILES,instance = product)
        if form.is_valid():
            form.save()
        else:
            form_errors = form.errors

        return redirect('Products:employee_view_product',product_id=product_id)
    else:
        product_form = EditProductForm(instance=product)
        return render(request, "edit_product.html",{'form':product_form,'product_id':product_id})
    

def combine_lists(list1,list2):
    combined_dict = defaultdict(int)

    for item in list1:
        combined_dict[item['date']] += item['total_quantity']

    for item in list2:
        combined_dict[item['date']] += item['total_quantity']

    combined_list = [{'date': date, 'total_quantity': total} for date, total in combined_dict.items()]

    return combined_list

def load_product_history_data(product_id):
    product = Product.objects.get(product_id=product_id)
    six_month_date = datetime.now() - timedelta(days=6*30)
    orders = True
    purchases = True
    try:
        orders_in_range = ProductInOrder.objects.filter(product=product,
                                                        order_info_object__order_date__range=[six_month_date, datetime.now()]) \
                                                        .order_by('order_info_object__order_date')

    except ProductInOrder.DoesNotExist:
        orders = False

    try:
        purchases_in_range = ProductInPurchase.objects.filter(product=product,
                                                            purchase_info_object__purchase_date__range=[six_month_date, datetime.now()]) \
                                                    .order_by('purchase_info_object__purchase_date')
    except ProductInPurchase.DoesNotExist:
        purchases = False

   
    # daily_order_results = list(orders_in_range.annotate(date=TruncDate('order_info_object__order_date')).values('date').annotate(total_quantity=Sum('quantity')).distinct())
    # daily_purchase_results = list(purchases_in_range.annotate(date=TruncDate('purchase_info_object__purchase_date')).values('date').annotate(total_quantity=Sum('quantity')))

    # weekly_order_results = list(orders_in_range.annotate(week=TruncWeek('order_info_object__order_date')).values('week').annotate(total_quantity=Sum('quantity')))
    # weekly_purchase_results = list(purchases_in_range.annotate(week=TruncWeek('purchase_info_object__purchase_date')).values('week').annotate(total_quantity=Sum('quantity')))

    # monthly_order_results = list(orders_in_range.annotate(month=TruncMonth('order_info_object__order_date')).values('month').annotate(total_quantity=Sum('quantity')))
    # monthly_purchase_results = list(purchases_in_range.annotate(month=TruncMonth('purchase_info_object__purchase_date')).values('month').annotate(total_quantity=Sum('quantity')))

    daily_orders_data = orders_in_range.annotate(date=TruncDate('order_info_object__order_date')).values('date', 'quantity')
    daily_order_results = {}

    for order in daily_orders_data:
        date = order['date'].strftime('%m-%d-%Y')
        quantity = order['quantity']
        if date in daily_order_results.keys():
            daily_order_results[date] += quantity
        else:
            daily_order_results[date] = quantity

    daily_purchases_data = purchases_in_range.annotate(date=TruncDate('purchase_info_object__purchase_date')).values('date','quantity')
    daily_purchase_results = {}

    for purchase in daily_purchases_data:
        date = purchase['date'].strftime('%m-%d-%Y')
        quantity = purchase['quantity']
        if date in daily_purchase_results.keys():
            daily_purchase_results[date] += quantity
        else:
            daily_purchase_results[date] = quantity


    weekly_orders_data = orders_in_range.annotate(week=TruncWeek('order_info_object__order_date')).values('week', 'quantity')
    weekly_order_results = {}

    for order in weekly_orders_data:
        week_start = order['week']
        week_end = week_start + timedelta(days=6)
        week = f"{week_start.strftime('%m-%d-%Y')} - {week_end.strftime('%m-%d-%Y')}"
        quantity = order['quantity']
        if week in weekly_order_results.keys():
            weekly_order_results[week] += quantity
        else:
            weekly_order_results[week] = quantity

    weekly_purchases_data = purchases_in_range.annotate(week=TruncWeek('purchase_info_object__purchase_date')).values('week','quantity')
    weekly_purchase_results = {}

    for purchase in weekly_purchases_data:
        week_start = purchase['week']
        week_end = week_start + timedelta(days=6)
        week = f"{week_start.strftime('%m-%d-%Y')} - {week_end.strftime('%m-%d-%Y')}"
        quantity = purchase['quantity']
        if week in weekly_purchase_results.keys():
            weekly_purchase_results[week] += quantity
        else:
            weekly_purchase_results[week] = quantity
    

    monthly_orders_data = orders_in_range.annotate(month=TruncMonth('order_info_object__order_date')).values('month', 'quantity')
    monthly_order_results = {}

    for order in monthly_orders_data:
        month = order['month'].strftime('%m-%Y')
        quantity = order['quantity']
        if month in monthly_order_results.keys():
            monthly_order_results[month] += quantity
        else:
            monthly_order_results[month] = quantity

    monthly_purchases_data = purchases_in_range.annotate(month=TruncMonth('purchase_info_object__purchase_date')).values('month','quantity')
    monthly_purchase_results = {}

    for purchase in monthly_purchases_data:
        month = purchase['month'].strftime('%m-%Y')
        quantity = purchase['quantity']
        if month in monthly_purchase_results.keys():
            monthly_purchase_results[month] += quantity
        else:
            monthly_purchase_results[month] = quantity


    
    
    


    overall_daily_total_results = {}
    all_dates = set(daily_order_results.keys()) | set(daily_purchase_results.keys())
    all_dates = sorted(all_dates)

    for date in all_dates:
        total_order_quantity = daily_order_results.get(date,0)
        total_purchase_quantity = daily_purchase_results.get(date,0)
        total_quantity = total_order_quantity + total_purchase_quantity

        overall_daily_total_results[date] = total_quantity




    overall_weekly_total_results = {}
    all_weeks = set(weekly_order_results.keys()) | set(weekly_purchase_results.keys())
    all_weeks = sorted(all_weeks)

    for week in all_weeks:
        total_order_quantity = weekly_order_results.get(week,0)
        total_purchase_quantity = weekly_purchase_results.get(week,0)
        total_quantity = total_order_quantity + total_purchase_quantity

        overall_weekly_total_results[week] = total_quantity



    overall_monthly_total_results = {}
    all_months = set(monthly_order_results.keys()) | set(monthly_purchase_results.keys())
    all_months = sorted(all_months)

    for month in all_months:
        total_order_quantity = monthly_order_results.get(month,0)
        total_purchase_quantity = monthly_purchase_results.get(month,0)
        total_quantity = total_order_quantity + total_purchase_quantity

        overall_monthly_total_results[month] = total_quantity


    num_days = 180
    num_weeks = 24  #TODO needs fixing this to find the true amount of weeks
    num_months = 6

    orders_daily_average = round(sum(daily_order_results.values()) / num_days,2)
    orders_weekly_average = round(sum(weekly_order_results.values()) / num_weeks,2)
    orders_monthly_average = round(sum(monthly_order_results.values()) / num_months,2)

    purchases_daily_average = round(sum(daily_purchase_results.values()) / num_days,2)
    purchases_weekly_average = round(sum(weekly_purchase_results.values()) / num_weeks,2)
    purchases_monthly_average = round(sum(monthly_purchase_results.values()) / num_months,2)

    overall_daily_average = round(sum(overall_daily_total_results.values()) / num_days,2)
    overall_weekly_average = round(sum(overall_weekly_total_results.values()) / num_weeks,2)
    overall_monthly_average = round(sum(overall_monthly_total_results.values()) / num_months,2)

    return_dict = {"orders_daily_average":orders_daily_average,
                   "orders_weekly_average":orders_weekly_average,
                   "orders_monthly_average":orders_monthly_average,
                   "purchases_daily_average":purchases_daily_average,
                   "purchases_weekly_average":purchases_weekly_average,
                   "purchases_monthly_average":purchases_monthly_average,
                   "overall_daily_average":overall_daily_average,
                   "overall_weekly_average":overall_weekly_average,
                   "overall_monthly_average":overall_monthly_average,
                   "orders_daily_total_results":daily_order_results,
                   "orders_weekly_total_results":weekly_order_results,
                   "orders_monthly_total_results":monthly_order_results,
                   "purchases_daily_total_results":daily_purchase_results,
                   "purchases_weekly_total_results":weekly_purchase_results,
                   "purchases_monthly_total_results":monthly_purchase_results,
                   "overall_daily_total_results":overall_daily_total_results,
                   "overall_weekly_total_results":overall_weekly_total_results,
                   "overall_monthly_total_results":overall_monthly_total_results
    }

    return return_dict

#This view and when the api is created will need the store_id as well. 
def employee_view_product(request,product_id):
    

    context = {"product_id": product_id}
    if request.method == "POST":
        product = Product.objects.get(product_id=product_id)
        
        product_history_data = load_product_history_data(product_id)
        
        order_averages = {"daily": product_history_data.get("orders_daily_average"),
                          "weekly": product_history_data.get("orders_weekly_average"),
                          "monthly": product_history_data.get("orders_monthly_average")}
        
        purchase_averages = {"daily": product_history_data.get("purchases_daily_average"),
                             "weekly": product_history_data.get("purchases_weekly_average"),
                             "monthly": product_history_data.get("purchases_monthly_average")}

        overall_averages = {"daily": product_history_data.get("overall_daily_average"),
                            "weekly": product_history_data.get("overall_weekly_average"),
                            "monthly": product_history_data.get("overall_monthly_average")}

        
        return JsonResponse({"product":product.to_dict(),
                             "order_averages": order_averages,
                             "purchase_averages": purchase_averages,
                             "overall_averages": overall_averages,
                             "graph_data": product_history_data})
    else:
        return render(request,"employee_view_product.html",context=context)

    # product = Product.objects.get(product_id=product_id)

    # data = load_product_history_data(product_id)
    
    # context={"product":product,
    #          "orders_averages":[data.get("orders_daily_average"),data.get("orders_weekly_average"),data.get("orders_monthly_average")],
    #          "purchases_averages":[data.get("purchases_daily_average"),data.get("purchases_weekly_average"),data.get("purchases_monthly_average")],
    #          "overall_averages":[data.get("overall_daily_average"),data.get("overall_weekly_average"),data.get("overall_monthly_average")]}
                
    # graph_data_list = ["orders_daily_total_results","orders_weekly_total_results","orders_monthly_total_results",
    #                    "purchases_daily_total_results","purchases_weekly_total_results","purchases_monthly_total_results",
    #                    "overall_daily_total_results","overall_weekly_total_results","overall_monthly_total_results"]

    # div_list = ["orders-daily-graph-div","orders-weekly-graph-div","orders-monthly-graph-div",
    #             "purchases-daily-graph-div","purchases-weekly-graph-div","purchases-monthly-graph-div",
    #             "overall-daily-graph-div","overall-weekly-graph-div","overall-monthly-graph-div"]
    
    # title_list = ["Daily Order Totals", "Weekly Order Totals", "Monthly Order Totals",
    #               "Daily Purchase Totals", "Weekly Purchase Totals", "Monthly Purchase Totals",
    #               "Daily Overall Totals", "Weekly Overall Totals", "Monthly Overall Tools"]
    
    

    # graph_info_lists = []
    # for index in range(len(graph_data_list)):
    #     queryset = data.get(graph_data_list[index])
    #     if queryset:
    #         new_list = [build_graph(data.get(graph_data_list[index])),div_list[index],title_list[index]]
    #         graph_info_lists.append(new_list)

    # context["graph_information"] = graph_info_lists

    

