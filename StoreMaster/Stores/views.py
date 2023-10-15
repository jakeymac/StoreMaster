from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return HttpResponse("Stores Home")

def register_store(request):
    print("HI THERE")
    if request.method == "POST":
        #Check if the user has opted to use a pre-existing manager or register a new one
        newRegistrationForm = StoreRegistrationForm(request.POST)
        errors = ""
        try:
            if newRegistrationForm.is_valid():
                existing_manager_val = newRegistrationForm.cleaned_data["manager"]

                newStore = Store(store_name=newRegistrationForm.cleaned_data["store_name"],
                                        address=newRegistrationForm.cleaned_data["store_address"],
                                        line_two=newRegistrationForm.cleaned_data["store_line_two"],
                                        city=newRegistrationForm.cleaned_data["store_city"],
                                        state=newRegistrationForm.cleaned_data["store_state"],
                                        zip=newRegistrationForm.cleaned_data["store_zip"])
                
                #If a pre-existing manager was not chosen
                if not existing_manager_val:
                    new_manager_info = {"first_name":newRegistrationForm.cleaned_data["manager_first_name"],
                                        "last_name":newRegistrationForm.cleaned_data["manager_last_name"],
                                        "email_address":newRegistrationForm.cleaned_data["manager_email_address"],
                                        "address":newRegistrationForm.cleaned_data["manager_address"],
                                        "line_two":newRegistrationForm.cleaned_data["manager_line_two"],
                                        "city":newRegistrationForm.cleaned_data["manager_city"],
                                        "state":newRegistrationForm.cleaned_data["manager_state"],
                                        "zip":newRegistrationForm.cleaned_data["manager_zip"],
                                        "username":newRegistrationForm.cleaned_data["manager_username"],
                                        "password":newRegistrationForm.cleaned_data["manager_password"],
                                        "other_information":newRegistrationForm.cleaned_data["manager_other_information"],
                                        "birthday":newRegistrationForm.cleaned_data["manager_birthday"]}
                    
                    new_user_form = UserRegistrationForm(initial=new_manager_info)

                    if new_user_form.is_valid():
                        newStore.save()
                        
                        user = User(username=newRegistrationForm.cleaned_data["manager_username"],
                                    password=newRegistrationForm.cleaned_data["manager_password"],
                                    emai=newRegistrationForm.cleaned_data["manager_email_address"])
                        
                        user.save()
                        
                        newManager = ManagerInfo(user=user,
                                                first_name=newRegistrationForm.cleaned_data["manager_first_name"],
                                                last_name=newRegistrationForm.cleaned_data["manager_last_name"],
                                                email_address=newRegistrationForm.cleaned_data["manager_last_name"],
                                                address=newRegistrationForm.cleaned_data["manager_address"],
                                                line_two=newRegistrationForm.cleaned_data["manager_line_two"],
                                                city=newRegistrationForm.cleaned_data["manager_city"],
                                                state=newRegistrationForm.cleaned_data["manager_state"],
                                                zip=newRegistrationForm.cleaned_data["manager_zip"],
                                                username=newRegistrationForm.cleaned_data["manager_username"],
                                                password=newRegistrationForm.cleaned_data["manager_password"],
                                                other_information=newRegistrationForm.cleaned_data["manager_other_information"],
                                                birthday=newRegistrationForm.cleaned_data["manager_birthday"],
                                                store=newStore)
        
                        newManager.save()
                    return HttpResponse("Valid FORM Time, created new objects")
                else:
                    newStore.save()
                    manager = newRegistrationForm.cleaned_data["manager"]
                    manager.store = newStore
                    manager.save()            


                    return HttpResponse("TESTINGGG")  
            else:
                return HttpResponse("ERROR:")
        
        
        except ValidationError as e:
            errors += f"{str(e)}\n"
        
        return HttpResponse(errors)
                
        
    else:
        clean_form = StoreRegistrationForm()
        return render(request, "register_store.html",{'form':clean_form})