from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from Stores.models import *
from Accounts.models import *
from .serializers import *

@api_view(['GET','POST','PUT','DELETE'])
def purchase_endpoint(request,id_type=None,id=None):
    if request.method == 'GET':
        if id_type is not None:
            if id_type == "store":
                if id is not None:
                    store = Store.objects.get(store_id=id)
                    purchases = Purchase.objects.filter(store=store)
                    purchase_serializer = PurchaseSerializer(purchases, many=True)
                    return Response({"purchases":purchase_serializer.data},status=status.HTTP_200_OK)
                
            else:
                return Response({"message": "Invalid id_type"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if id is not None:
                purchase = Purchase.objects.get(purchase_id = id)
                purchase_serializer = PurchaseSerializer(purchase)
                return Response({"purchase": purchase_serializer.data}, status=status.HTTP_200_OK)

            else:
                purchases = Purchase.objects.all()
                purchase_serializer = PurchaseSerializer(purchases, many=True)
                return Response({"purchases":purchase_serializer.data},status=status.HTTP_200_OK)