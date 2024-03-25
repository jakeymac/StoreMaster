from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from datetime import datetime, timedelta
import math

from .models import *
from Stores.models import *
from .serializers import *

@api_view(['GET','POST','PUT','DELETE'])
def product_endpoint(request,id_type=None,id=None,is_active=None):
    if request.method == 'GET':
        if id_type is not None:
            if id_type == "store":
                if id is not None:
                    store = Store.objects.get(store_id=id)
                    if is_active is None:
                        #Don't filter for active or inactive products, return all products in the store
                        products = Product.objects.filter(store=store)

                    elif is_active.lower() == 'true' or is_active.lower() == 'false':
                        products = Product.objects.filter(store=store,is_active=(is_active.lower() == 'true'))

                    else:
                        return Response({"message": "Invalid is_active value"}, status=status.HTTP_400_BAD_REQUEST)

                    products_low_in_stock = []
                    for product in products:
                        if product.product_stock <= product.low_stock_quantity:
                            products_low_in_stock.append(product)
                    
                    products_low_in_stock_serializer = ProductSerializer(products_low_in_stock, many=True)
                    product_serializer = ProductSerializer(products, many=True)

                    return Response({"products": product_serializer.data,
                                    "products_low_in_stock": products_low_in_stock_serializer.data}, 
                                    status=status.HTTP_200_OK)

            else:
                return Response({"message": "Invalid id_type"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if id is not None:
                
                product = Product.objects.get(product_id=id)
                product_serializer = ProductSerializer(product)
                return Response({"product": product_serializer.data}, status=status.HTTP_200_OK)
                
            else:
                if is_active is None:
                    products = Product.objects.all()

                elif is_active.lower() == 'true' or is_active.lower() == 'false':
                    products = Product.objects.filter(is_active=(is_active.lower() == 'true'))
                else:
                    return Response({"message": "Invalid is_active value"}, status=status.HTTP_400_BAD_REQUEST)

                product_serializer = ProductSerializer(products, many=True)
                return Response({"product": product_serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # import pdb
        # pdb.set_trace()
        return delete_product(request,id,id_type)

@permission_classes([IsAuthenticated])
def delete_product(request,id,id_type=None):
    if request.user.userinfo.account_type != "customer":
        if id_type is None:
            if id is not None:
                product = Product.objects.get(product_id = id)
                try:
                    product.is_active = False
                    product.save()
                    product_serializer = ProductSerializer(product)
                    
                    return Response({"message": "Successfully deleted product","product": product_serializer.data}, status=status.HTTP_200_OK)

                except Exception as e:
                    return Response({"message":"Error deleting product"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            #This will serve to delete all products in a store
            pass


@api_view(['GET','POST','PUT'])
def product_in_order_endpoint(request,id=None):
    if request.user.is_authenticated:
        if id is not None:
            order = Order.objects.get(order_id=id)
            products_in_order = ProductInOrder.objects.filter(order_info_object = order)
            products_in_order_serializer = ProductInOrderSerializer(products_in_order, many=True)
            return Response({"products_in_order": products_in_order_serializer.data}, status=status.HTTP_200_OK)

        else:
            products_in_orders = ProductInOrder.objects.all()
            products_in_order_serializer = ProductInOrderSerializer(products_in_orders, many=True)
            return Response({"products_in_orders": products_in_orders_serializer.data}, status=status.HTTP_200_OK)
        
    else:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def product_history_endpoint(request,id=None):
    # TODO Could make a public version of this, without providing any order/purchase information of users or employees.
    if request.user.is_authenticated:
        if id is not None:
            product = Product.objects.get(product_id=id)
            product_serializer = ProductSerializer(product)

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

            product_history = {"orders_daily_average":orders_daily_average,
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

            

            return Response({"product_history_data": product_history, "product":product_serializer.data}, status=status.HTTP_200_OK)                                                                     

        else:
            return Response({"message": "Only product_id GET request are supported as of right now"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


