import time
import json
import random
import torch
import torch.nn as nn
import paho.mqtt.client as mqtt

# 1. DEFINE THE AI MODEL (PyTorch)
class FatigueNet(nn.Module):
    def __init__(self):
        super(FatigueNet, self).__init__()
        # Simple Linear layer to simulate a classifier
        self.fc = nn.Linear(10, 1) 

    def forward(self, x):
        return torch.sigmoid(self.fc(x))

# Initialize Model (Mocking weights for demo)
model = FatigueNet()
model.eval()

# 2. SETUP MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60) # Connects to Docker exposed port

print("Starting Engine...")

while True:
    # 3. SIMULATE COMPUTER VISION DATA
    # In real life, 'features' would come from CNN processing of a camera frame
    # Here, we generate random tensors representing eye-closure rates
    dummy_camera_features = torch.randn(10)
    
    with torch.no_grad():
        # Get AI prediction (0 = Alert, 1 = Asleep)
        fatigue_score = model(dummy_camera_features).item()

    # 4. SIMULATE SENSORS
    # Add noise to temp to prove our backend smoothing works!
    base_temp = 90
    noise = random.randint(-5, 15) 
    
    payload = {
        "vehicle_id": "BMW-X3-TEST",
        "speed": random.randint(60, 120),
        "engine_temp": base_temp + noise,
        "fatigue_score": round(fatigue_score, 4)
    }

    client.publish("car/sensors", json.dumps(payload))
    print(f"Telemetry Sent: {payload}")
    time.sleep(1)