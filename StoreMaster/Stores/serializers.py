from rest_framework import serializers
from .models import *

class StoreSerializer(serializers.ModelSerializer):
    line_two = serializers.CharField(required=False)
    class Meta:
        model = Store
        fields = ['store_id', 'store_name', 'address', 'line_two', 'city', 'state', 'zip']