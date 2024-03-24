from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from Stores.models import *
from .serializers import *

@api_view(['GET','POST','PUT','DELETE'])
def product_endpoint(request,id_type=None,id=None):
    if request.method == 'GET':
        if id_type is not None:
            if id_type == "store":
                if id is not None:
                    store = Store.objects.get(store_id=id)
                    products = Product.objects.filter(store=store)

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
                products = Product.objects.all()
                product_serializer = ProductSerializer(products, many=True)
                return Response({"product": product_serializer.data}, status=status.HTTP_200_OK)

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


