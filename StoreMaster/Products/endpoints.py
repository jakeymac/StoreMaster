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
                    if id_type == "store":
                        store = Store.objects.get(store_id=id)
                        products = Product.objects.filter(store=store)
                        product_serializer = ProductSerializer(products, many=True)
                        return Response({"products": product_serializer.data}, status=status.HTTP_200_OK)
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

