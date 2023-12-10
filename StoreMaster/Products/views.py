from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from Products.forms import EditProductForm, NewProductForm

from Products.models import *
from Stores.models import *

from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from datetime import datetime, timedelta
import math

from collections import defaultdict
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64



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
            
        return redirect('Products:employee_view_product',product_id=product_id)
    else:
        print("Not POST step 2")
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
        print("Made ittt")
    except ProductInOrder.DoesNotExist:
        orders = False
        print("nailed itttt")
    try:
        purchases_in_range = ProductInPurchase.objects.filter(product=product,
                                                            purchase_info_object__purchase_date__range=[six_month_date, datetime.now()]) \
                                                    .order_by('purchase_info_object__purchase_date')
        print("Made ittt")
    except ProductInPurchase.DoesNotExist:
        purchases = False
        print("nailed ittt")


    order_daily_total_results = orders_in_range.annotate(date_group=TruncDate('order_info_object__order_date')).values('date_group').annotate(total_quantity=Sum('quantity'))
    purchase_daily_total_results = purchases_in_range.annotate(date_group=TruncDate('purchase_info_object__purchase_date')).values('date_group').annotate(total_quantity=Sum('quantity'))

    order_weekly_total_results = orders_in_range.annotate(week_group=TruncWeek('order_info_object__order_date')).values('week_group').annotate(total_quantity=Sum('quantity'))
    purchase_weekly_total_results = purchases_in_range.annotate(week_group=TruncWeek('purchase_info_object__purchase_date')).values('week_group').annotate(total_quantity=Sum('quantity'))

    order_monthly_total_results = orders_in_range.annotate(month_group=TruncMonth('order_info_object__order_date')).values('month_group').annotate(total_quantity=Sum('quantity'))
    purchase_monthly_total_results = purchases_in_range.annotate(month_group=TruncMonth('purchase_info_object__purchase_date')).values('month_group').annotate(total_quantity=Sum('quantity'))

    order_totals_dict = {entry['date_group']: {'total_quantity_orders': entry['total_quantity']} for entry in order_daily_total_results}    
    purchase_totals_dict = {entry['date_group']: {'total_quantity_purchases': entry['total_quantity']} for entry in purchase_daily_total_results} 
    
    overall_daily_total_results = []
    all_dates = set(order_totals_dict.keys()) | set(purchase_totals_dict.keys())
    all_dates = sorted(all_dates)
    print(all_dates)
    for date in all_dates:
        overall_daily_total_results.append({
            'date_group':date,
            **order_totals_dict.get(date, {'total_quantity_orders':0}),
            **purchase_totals_dict.get(date, {'total_quantity_purchases':0}),
            'total_quantity': order_totals_dict.get(date, {'total_quantity_orders': 0})['total_quantity_orders'] + 
                                       purchase_totals_dict.get(date, {'total_quantity_purchases': 0})['total_quantity_purchases'],
        })

    order_totals_dict = {entry['week_group']: {'total_quantity_orders': entry['total_quantity']} for entry in order_weekly_total_results}    
    purchase_totals_dict = {entry['week_group']: {'total_quantity_purchases': entry['total_quantity']} for entry in purchase_weekly_total_results}
    
    overall_weekly_total_results = []
    all_weeks = set(order_totals_dict.keys()) | set(purchase_totals_dict.keys())
    all_weeks = sorted(all_weeks)
    for week in all_weeks:
        overall_weekly_total_results.append({
            'week_group':week,
            **order_totals_dict.get(week, {'total_quantity_orders':0}),
            **purchase_totals_dict.get(week, {'total_quantity_purchases':0}),
            'total_quantity': order_totals_dict.get(week, {'total_quantity_orders': 0})['total_quantity_orders'] + 
                                       purchase_totals_dict.get(week, {'total_quantity_purchases': 0})['total_quantity_purchases'],
        })


    order_totals_dict = {entry['month_group']: {'total_quantity_orders': entry['total_quantity']} for entry in order_monthly_total_results}    
    purchase_totals_dict = {entry['month_group']: {'total_quantity_purchases': entry['total_quantity']} for entry in purchase_monthly_total_results} 
    
    overall_monthly_total_results = []
    all_months = set(order_totals_dict.keys()) | set(purchase_totals_dict.keys())
    all_months = sorted(all_months)
    for month in all_months:
        overall_monthly_total_results.append({
            'month_group':month,
            **order_totals_dict.get(month, {'total_quantity_orders':0}),
            **purchase_totals_dict.get(month, {'total_quantity_purchases':0}),
            'total_quantity': order_totals_dict.get(month, {'total_quantity_orders': 0})['total_quantity_orders'] + 
                                       purchase_totals_dict.get(month, {'total_quantity_purchases': 0})['total_quantity_purchases'],
        })


    num_days = 180
    num_weeks = 24  #TODO needs fixing this to find the true amount of weeks
    num_months = 6

    

    orders_daily_average = round(sum(entry['total_quantity'] for entry in order_daily_total_results) / num_days,2)
    orders_weekly_average = round(sum(entry['total_quantity'] for entry in order_weekly_total_results) / num_weeks,2)
    orders_monthly_average = round(sum(entry['total_quantity'] for entry in order_monthly_total_results) / num_months,2)

    purchases_daily_average = round(sum(entry['total_quantity'] for entry in purchase_daily_total_results) / num_days,2)
    purchases_weekly_average = round(sum(entry['total_quantity'] for entry in purchase_weekly_total_results) / num_weeks,2)
    purchases_monthly_average = round(sum(entry['total_quantity'] for entry in purchase_monthly_total_results) / num_months,2)

    overall_daily_average = round(sum(entry['total_quantity'] for entry in overall_daily_total_results) / num_days,2)
    overall_weekly_average = round(sum(entry['total_quantity'] for entry in overall_weekly_total_results) / num_weeks,2)
    overall_monthly_average = round(sum(entry['total_quantity'] for entry in overall_monthly_total_results) / num_months,2)

    return_dict = {"orders_daily_average":orders_daily_average,
                   "orders_weekly_average":orders_weekly_average,
                   "orders_monthly_average":orders_monthly_average,
                   "purchases_daily_average":purchases_daily_average,
                   "purchases_weekly_average":purchases_weekly_average,
                   "purchases_monthly_average":purchases_monthly_average,
                   "overall_daily_average":overall_daily_average,
                   "overall_weekly_average":overall_weekly_average,
                   "overall_monthly_average":overall_monthly_average,
                   "orders_daily_total_results":order_daily_total_results,
                   "orders_weekly_total_results":order_weekly_total_results,
                   "orders_monthly_total_results":order_monthly_total_results,
                   "purchases_daily_total_results":purchase_daily_total_results,
                   "purchases_weekly_total_results":purchase_weekly_total_results,
                   "purchases_monthly_total_results":purchase_monthly_total_results,
                   "overall_daily_total_results":overall_daily_total_results,
                   "overall_weekly_total_results":overall_weekly_total_results,
                   "overall_monthly_total_results":overall_monthly_total_results 
    }

    return return_dict

def build_graph(queryset):
    group_name = list(queryset[0].keys())[0]

    title_conversion_dict = {"date":"Day",
                             "week":"Week",
                             "month":"Month"}
    
    
    time_title = title_conversion_dict.get(group_name.split("_")[0])
    
    if time_title == "Week":
        times = [f"Week {time_group[group_name].strftime('%U')} ({time_group[group_name].strftime('%B %dth, %Y')})"
                for time_group in queryset]
    elif time_title == "Month":
        times = [time_group[group_name].strftime('%B %dth, %Y') for time_group in queryset]
    else:
        times = [time_group[group_name].strftime('%B %dth, %Y') for time_group in queryset]

    values = [entry["total_quantity"] for entry in queryset]
    
    data = {time_title:times,"Values":values}

    fig, ax = plt.subplots(figsize=(12,7))

    ax.plot(data[time_title],data["Values"])
                            
    image_stream = BytesIO()
    plt.savefig(image_stream,format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()
    return image_base64


def employee_view_product(request,product_id):
    product = Product.objects.get(product_id=product_id)

    data = load_product_history_data(product_id)
    
    context={"product":product,
             "orders_averages":[data.get("orders_daily_average"),data.get("orders_weekly_average"),data.get("orders_monthly_average")],
             "purchases_averages":[data.get("purchases_daily_average"),data.get("purchases_weekly_average"),data.get("purchases_monthly_average")],
             "overall_averages":[data.get("overall_daily_average"),data.get("overall_weekly_average"),data.get("overall_monthly_average")]}
                
    graph_data_list = ["orders_daily_total_results","orders_weekly_total_results","orders_monthly_total_results",
                       "purchases_daily_total_results","purchases_weekly_total_results","purchases_monthly_total_results",
                       "overall_daily_total_results","overall_weekly_total_results","overall_monthly_total_results"]

    div_list = ["orders-daily-graph-div","orders-weekly-graph-div","orders-monthly-graph-div",
                "purchases-daily-graph-div","purchases-weekly-graph-div","purchases-monthly-graph-div",
                "overall-daily-graph-div","overall-weekly-graph-div","overall-monthly-graph-div"]
    
    title_list = ["Daily Order Totals", "Weekly Order Totals", "Monthly Order Totals",
                  "Daily Purchase Totals", "Weekly Purchase Totals", "Monthly Purchase Totals",
                  "Daily Overall Totals", "Weekly Overall Totals", "Monthly Overall Tools"]
    
    

    graph_info_lists = []
    for index in range(len(graph_data_list)):
        queryset = data.get(graph_data_list[index])
        if queryset:
            new_list = [build_graph(data.get(graph_data_list[index])),div_list[index],title_list[index]]
            graph_info_lists.append(new_list)

    context["graph_information"] = graph_info_lists

    

    return render(request,"employee_view_product.html",context=context)
