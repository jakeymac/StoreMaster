from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from Stores.models import *
from .serializers import *

@api_view(['GET', 'POST','PUT','DELETE'])
def order_endpoint(request, id_type=None, id=None):
    if request.method == 'GET':
        if id_type is not None:
            if id_type == "store":
                if id is not None:
                    store = Store.objects.get(store_id = id)
                    orders = Order.objects.filter(store=store)
                    order_serializer = OrderSerializer(orders, many=True)
                    return Response({"orders": order_serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Invalid id_type"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if id is not None:
                order = Order.objects.get(order_id = id)
                order_serializer = OrderSerializer(order)
                return Response({"order": order_serializer.data}, status=status.HTTP_200_OK)

            else:
                orders = Order.objects.all()
                order_serializer = OrderSerializer(orders, many=True)
                return Response({"orders": order_serializer.data}, status=status.HTTP_200_OK)
