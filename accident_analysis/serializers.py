from rest_framework import serializers
from .models import Accidents, Vehicles

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

class AccidentSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Accidents
        fields = '__all__'
