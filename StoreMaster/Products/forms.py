from django import forms
from django.core.exceptions import ValidationError

from .models import Product, ProductInOrder
from Stores.models import Store

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'store': forms.HiddenInput()
        }

        
    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data["product_name"]
        store = cleaned_data["store"]

        return cleaned_data


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 

        widgets = {
            'store': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data["product_name"]
        store = cleaned_data["store"]
        
        if Product.objects.filter(product_name=product_name,store=store).exclude(product_id=self.instance.product_id).exists():
            raise ValidationError("A product with this name already exists at that store")
            
        return cleaned_data


class EditProductOrderForm(forms.Form):
    pass

