# serializers.py
from rest_framework import serializers
from .models import VehicleTelemetry

class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTelemetry
        fields = '__all__'