Smart Fleet: AI-Powered Telemetry Pipeline

Executive Summary

Smart Fleet is a full-stack IoT ingestion pipeline designed to monitor vehicle telemetry and driver safety in real-time.

Unlike standard CRUD apps, this project simulates an Edge-to-Cloud architecture suitable for industrial use cases (e.g., Mining Fleet Management or Automotive Telemetry). It features a Python-based edge simulator using PyTorch for driver fatigue detection, utilizes MQTT for high-throughput messaging, and implements Sliding Window Algorithms within Django to sanitize noisy sensor data before storage.

Architecture

The system is fully containerized using Docker Compose and consists of four microservices:

Edge Device (Simulator): A Python script simulating vehicle sensors (Speed, RPM) and running a lightweight PyTorch neural network to detect driver drowsiness (Computer Vision logic).

Broker (Mosquitto): Handles asynchronous communication between the fleet and the backend via MQTT.

Backend (Django): Ingests data streams, performs O(1) algorithmic smoothing on sensor readings, and exposes a REST API.

Analytics (PostgreSQL & Grafana): Uses Window Functions for historical anomaly detection and real-time visualization.

Tech Stack & Skills Demonstrated
Domain	                Technology	                Implementation Detail
Backend Engineering	    Django & Python	            Custom Management Commands for MQTT   
                                                    ingestion; 
                                                    Async worker pattern.                         
DevOps	                Docker	                    Full Infrastructure-as-Code (IaC)     
                                                    setup;    
                                                    multi-container orchestration.
Data Structures (DSA)	Python(Collections)	        Implemented a Sliding Window (Deque)  
                                                    algorithm to calculate moving averages of engine temperature to reduce sensor noise.
AI / Machine Learning	PyTorch	                    Simulated edge-inference for driver 
                                                    fatigue detection (Binary Classification).
Database	            PostgreSQL	                utilized SQL Window Functions (LAG, 
                                                    OVER, PARTITION) to calculate temperature deltas and identify risk events.
IoT Protocols	        MQTT	                    Pub/Sub architecture using paho-mqtt and 
                                                    Eclipse Mosquitto.

Getting Started
Prerequisites: Docker and Docker Compose.

Clone the Repository

Bash

git clone https://github.com/yourusername/smart-fleet.git
cd smart-fleet
Launch Infrastructure Spins up Postgres, Mosquitto, Django, and Grafana.

Bash

docker-compose up --build
Start the Ingestion Worker In a new terminal:

Bash

docker-compose exec backend python manage.py listen_mqtt
Drive the Car (Start Simulator) In a host terminal (requires local python env):

Bash

pip install torch paho-mqtt
python edge_device/simulator.py

Technical Highlights
1. Algorithmic Data Smoothing (DSA)
Raw sensor data in industrial environments is noisy. Instead of writing every erratic value to the DB, I implemented a Sliding Window algorithm in the ingestion layer.

Python

# snippet from listen_mqtt.py
if v_id not in self.temp_windows:
    self.temp_windows[v_id] = deque(maxlen=5) # O(1) pops

self.temp_windows[v_id].append(raw_temp)
smoothed = mean(self.temp_windows[v_id])
2. Advanced SQL Analytics
To detect sudden engine temperature spikes that indicate cooling failure, I utilized PostgreSQL Window Functions rather than inefficient Python loops.

SQL

-- View generated in DB
SELECT 
    vehicle_id, 
    timestamp,
    engine_temp - LAG(engine_temp) OVER (PARTITION BY vehicle_id ORDER BY timestamp) as temp_spike
FROM core_vehicletelemetry;
Dashboard
Access Grafana at http://localhost:3000 (Default: admin/admin). Configuration: Connect to Postgres host db.

Future Roadmap
Kubernetes: Migrate from Docker Compose to K8s for auto-scaling the ingestion workers.

Celery: Decouple the MQTT listener further using Redis and Celery tasks.

Real Computer Vision: Integrate OpenCV to use the webcam for actual driver eye-tracking.