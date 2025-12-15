from rest_framework import serializers
from .models import Accidents, Vehicles

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

class AccidentSerializer(serializers.ModelSerializer):
    vehicles = serializers.PrimaryKeyRelatedField(many=True, queryset=Vehicles.objects.all())

    class Meta:
        model = Accidents
        fields = '__all__'
