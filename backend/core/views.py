# views.py
from rest_framework import viewsets
from .models import VehicleTelemetry
from .serializers import TelemetrySerializer

class TelemetryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API Endpoint for external systems (e.g., Fleet Manager Mobile App)
    to query vehicle history.
    """
    queryset = VehicleTelemetry.objects.all().order_by('-timestamp')
    serializer_class = TelemetrySerializer