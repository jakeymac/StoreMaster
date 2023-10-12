from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return HttpResponse("Stores Home")

def register_store(request):
    if request.method == "POST":
        pass
    else:
        clean_form = StoreRegistrationForm()
        return render(request, "register_store.html",{'form':clean_form})
    return HttpResponse("Register Store Page")