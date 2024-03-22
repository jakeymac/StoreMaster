from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .models import *
from .serializers import *

import json

model_dict = {"manager":ManagerInfo,
              "admin":AdminInfo,
              "employee":EmployeeInfo,
              "customer":CustomerInfo}


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
            pass
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

        