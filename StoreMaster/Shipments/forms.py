from django import forms
from django.forms.widgets import DateInput
from .models import Shipment


class NewShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = "__all__"
        widgets = {
            "destination_store":forms.HiddenInput(),
            "shipped_date":forms.SelectDateWidget(years=range(2000,2030)),
            "expected_date":forms.SelectDateWidget(years=range(2000,2030))
        }


class ShipmentJSONFileForm(forms.Form):
    json_file = forms.FileField()
