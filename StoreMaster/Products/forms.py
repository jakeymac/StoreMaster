from django import forms
from django.core.exceptions import ValidationError

from .models import Product
from Stores.models import Store

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['store']
        #fields = ['store','product_stock','product_image','product_name','product_description','product_price','product_location']
    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data["product_name"]
        store = cleaned_data["store"]

        if Product.objects.filter(product_name=product_name,store=store).exists():
            raise ValidationError("A product with this name already exists at that store")
 
        return cleaned_data


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude  = ['store']
        #fields = ['store','product_stock','product_image','product_name','product_description','product_price','product_location']


    def __init__(self,*args,**kwargs):
        store = kwargs.pop('store',None)
        super().__init__(*args,**kwargs)

        if store:
            self.fields['store'] = forms.ModelChoiceField(queryset=Store.objects.all(), initial=store, widget=forms.HiddenInput())


    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data["product_name"]
        store = cleaned_data["store"]
        
        if Product.objects.filter(product_name=product_name,store=store).exclude(product_id=self.instance.product_id).exists():
            raise ValidationError("A product with this name already exists at that store")
 
        return cleaned_data
