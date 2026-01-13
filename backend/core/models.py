from django.db import models

class VehicleTelemetry(models.Model):
    vehicle_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.IntegerField()
    engine_temp = models.FloatField()
    smoothed_temp = models.FloatField(help_text="Moving Average for Noise Reduction")
    driver_fatigue_score = models.FloatField()
    is_anomaly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle_id} - {self.timestamp}"