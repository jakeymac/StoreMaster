from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .models import *
from .serializers import *
from Stores.serializers import *

import json

model_dict = {"manager":ManagerInfo,
              "admin":AdminInfo,
              "employee":EmployeeInfo,
              "customer":CustomerInfo}

serializer_dict = {"manager":ManagerInfoSerializer,
                    "admin":AdminInfoSerializer,
                    "employee":EmployeeInfoSerializer,
                    "customer":CustomerInfoSerializer}

@api_view(['GET'])
def logged_in_account_endpoint(request):
    """Endpoint for getting the account information for the user currently logged in """
    if request.user.is_authenticated:
        account_info_object_type = model_dict.get(request.user.userinfo.account_type)
        account_info_object = account_info_object_type.objects.get(user=request.user.userinfo.user)
        account_serializer = serializer_dict.get(request.user.userinfo.account_type)(account_info_object)
        return Response({"account_info":account_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No user currently logged in"})
    print(request.user)
    user = User.objects.filter(user=request.user)

@api_view(['GET'])
def customer_endpoint(request,store_id=None):
    if request.user.is_authenticated:
        if store_id is not None:
            store = Store.objects.get(store_id=store_id)
            customers = CustomerInfo.objects.filter(store=store)
            customer_serializer = CustomerInfoSerializer(customers,many=True)
            return Response({"customers": customer_serializer.data}, status=status.HTTP_200_OK)
        else:
            customers = CustomerInfo.objects.all()
            customer_serializer = CustomerInfoSerializer(customers, many=True)
            return Response({"customers": customer_serializer.data}, status=status.HTTP_200_OK)

    else:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def employee_endpoint(request,store_id=None):
    if request.user.is_authenticated:
        if store_id is not None:
            store = Store.objects.get(store_id=store_id)
            employees = EmployeeInfo.objects.filter(store=store)
            employee_serializer = EmployeeInfoSerializer(employees,many=True)
            return Response({"employees": employee_serializer.data}, status=status.HTTP_200_OK)
        else:
            employees = EmployeeInfo.objects.all()
            employee_serializer = EmployeeInfoSerializer(employees,many=True)
            return Response({"employees": employee_serializer.data}, status=status.HTTP_200_OK)

    else:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def manager_endpoint(request,store_id=None):
    if request.user.is_authenticated:
        if store_id is not None:
            store = Store.objects.get(store_id=store_id)
            manages = ManagerInfo.objects.filter(store=store)
            manager_serializer = ManagerInfoSerializer(managers,many=True)
            return Response({"managers": manager_serializer.data}, status=status.HTTP_200_OK)
        else:
            managers = ManagerInfo.objects.all()
            manager_serializer = ManagerInfoSerializer(managers,many=True)
            return Response({"managers": manager_serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['GET','POST','PUT','DELETE'])
def account_endpoint(request,account_id=None):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if account_id is None:
                customers = CustomerInfo.objects.all()
                employees = EmployeeInfo.objects.all()
                managers = ManagerInfo.objects.all()
                admins = AdminInfo.objects.all()

                customer_serializer = CustomerInfoSerializer(customers, many=True)
                employee_serializer = EmployeeInfoSerializer(employees, many=True)
                manager_serializer = ManagerInfoSerializer(managers, many=True)
                #TODO make this more secure and add a checker to see if the user requesting is an admin
                admin_serializer = AdminInfoSerializer(admins, many=True)

                return Response({"customers": customer_serializer.data, 
                                 "employees": employee_serializer.data,
                                 "managers": manager_serializer.data,
                                 "admins": admin_serializer.data})

            else:
                user = User.objects.get(id=account_id)
                if CustomerInfo.objects.filter(user=user).exists():
                    customer = CustomerInfo.objects.get(user=user)
                    customer_serializer = CustomerInfoSerializer(customer)
                    return Response({"account_data": customer_serializer.data}, status.HTTP_200_OK)
                elif EmployeeInfo.objects.filter(user=user).exists():
                    employee = EmployeeInfo.objects.get(user=user)
                    employee_serializer = EmployeeInfoSerializer(employee)
                    return Response({"account_data": employee_serializer.data}, status.HTTP_200_OK)
                elif ManagerInfo.objects.filter(user=user).exists():
                    manager = ManagerInfo.objects.get(user=user)
                    manager_serializer = ManagerInfoSerializer(manager)
                    return Response({"account_data": manager_serializer.data}, status.HTTP_200_OK)
                elif AdminInfo.objects.filter(user=user).exists():
                    admin = AdminInfo.objects.get(user=user)
                    admin_serializer = AdminInfoSerializer(admin)
                    return Response({"account_data": admin_serializer.data}, status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'POST':
            pass
        elif request.method == 'PUT':
            data = json.loads(request.body)
            user_data = data["user"]
            account_data = data["account_data"]
            messages = []
            success = True
            try:
                with transaction.atomic():  
                    user = User.objects.get(pk=user_data["id"])
                    user_serializer = UserSerializer(user, data=user_data)
                    if user_serializer.is_valid():
                        user_serializer.save()

                        store = Store.objects.get(store_id=account_data["store_id"])
                        account_data["store"] = store
                        account_data["user"] = user

                        account_type = account_data["account_type"]
                        account_instance = model_dict.get(account_type).objects.get(user=user)
                        account_serializer = serializer_dict.get(account_type)(account_instance, data=account_data)
                        if account_serializer.is_valid():
                            account_serializer.save()
                            messages.append("Successfully saved changes")
                            return_status = status.HTTP_200_OK
                        else:
                            print("Error here: ")
                            for error in account_serializer.errors.items():
                                print(error)
                            messages.append(account_serializer.errors)
                            return_status = status.status.HTTP_400_BAD_REQUEST
                    else:
                        for error in user_serializer.errors.items():
                            messages.append(str(error[1]))
                        return_status = status.HTTP_400_BAD_REQUEST

            except Exception as e:
                # Handle any unexpected exceptions
                messages.append("An error occurred: " + str(e))
                return_status = status.HTTP_500_INTERNAL_SERVER_ERROR

            return Response({"messages": messages}, status=return_status)


        elif request.method == 'DELETE':
            pass
    else:
        pass

def edit_employee_endpoint(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            new_employee_info = json.loads(request.body)
            print(new_employee_info)
            employee_id = new_employee_info["employee_id"]
            messages = []
            success = True
            if User.objects.filter(username=new_employee_info["username"]).exclude(pk=employee_id).exists():
                messages.append("username already exists")
                success = False
            
            if User.objects.filter(email=new_employee_info["email"]).exclude(pk=employee_id).exists():
                messages.append("email address already exists")
                success = False

            if success:
                user = User.objects.get(id=employee_id)
                employee_model = model_dict.get(new_employee_info["account_type"])
                employee = employee_model.objects.get(user = user)
                
                user.username = new_employee_info["username"]
                user.password = new_employee_info["password"]
                user.email = new_employee_info["email"]
                user.save()

                employee.username = new_employee_info["username"]
                employee.password = new_employee_info["password"]
                employee.first_name = new_employee_info["first_name"]
                employee.last_name = new_employee_info["last_name"]
                employee.email_address = new_employee_info["email"]
                employee.address = new_employee_info["address"]
                employee.line_two = new_employee_info["line_two"]
                employee.city = new_employee_info["city"]
                employee.state = new_employee_info["state"]
                employee.zip = new_employee_info["zip"]
                employee.store_id = new_employee_info["store_id"]
                employee.other_information = new_employee_info["other_information"]
                employee.birthday = new_employee_info["birthday"]
                employee.account_type = new_employee_info["account_type"]
                if "stock_notifications" in new_employee_info:
                    employee.stock_notifications = new_employee_info["stock_notifications"]
                
                employee.save()
                print(employee)

            return JsonResponse({"messages": messages,
                                "success": success})
    else:
        return JsonResponse({"message": "User not authenticated"})

        