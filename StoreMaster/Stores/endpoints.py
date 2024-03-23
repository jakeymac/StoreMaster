from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

import json
@api_view(['GET','POST','PUT','DELETE'])
def store_endpoint(request,store_id=None):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if store_id is None:
                stores = Store.objects.all()
                store_serializer = StoreSerializer(stores, many=True)
                return Response({"stores": store_serializer.data}, status=status.HTTP_200_OK)
            else:

                pass

        elif request.method == 'POST':
            pass
        elif request.method == 'PUT':
            print("Ok let's go")
            pass
        elif request.method == 'DELETE':
            pass
    else:   
        pass