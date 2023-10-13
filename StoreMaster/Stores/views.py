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
        if newRegistrationForm.is_valid():
            return HttpResponse("Valid FORM Time")
        
    else:
        clean_form = StoreRegistrationForm()
        return render(request, "register_store.html",{'form':clean_form})