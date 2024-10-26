from rest_framework import serializers
from .models import Bill, BillType

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class BillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillType
        fields = '__all__'


