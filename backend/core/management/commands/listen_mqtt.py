import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from collections import deque
from statistics import mean
from core.models import VehicleTelemetry

class Command(BaseCommand):
    help = 'Listens to MQTT car/sensors topic and saves to DB'

    # DSA: Sliding Window for Rolling Average (Size 5)
    # We use a Dictionary of Deques to handle multiple cars simultaneously
    temp_windows = {} 

    def handle(self, *args, **options):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.connect("mqtt", 1883, 60) # Connects to the Docker service named 'mqtt'
        client.subscribe("car/sensors")
        print("Listening for IoT data...")
        client.loop_forever()

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        v_id = payload['vehicle_id']
        raw_temp = payload['engine_temp']

        # --- THE ALGORITHM ---
        if v_id not in self.temp_windows:
            self.temp_windows[v_id] = deque(maxlen=5)
        
        self.temp_windows[v_id].append(raw_temp)
        smoothed = mean(self.temp_windows[v_id])
        # ---------------------

        # Save to DB
        VehicleTelemetry.objects.create(
            vehicle_id=v_id,
            speed=payload['speed'],
            engine_temp=raw_temp,
            smoothed_temp=smoothed,
            driver_fatigue_score=payload['fatigue_score']
        )
        print(f"Saved: {v_id} | Raw: {raw_temp} | Smooth: {smoothed}")