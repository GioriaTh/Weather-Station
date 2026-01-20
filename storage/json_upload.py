import json
import requests

class JSONUploader:
    def __init__(self, endpoint_url, timeout=10):
        self.endpoint_url = endpoint_url
        self.timeout = timeout

    def upload_measurement(self, temperature, humidity, soil_moisture, rainfall, rain_rate, timestamp):
        payload = {
            "timestamp": timestamp,
            "temperature_c": temperature,
            "humidity_percent": humidity,
            "soil_moisture": soil_moisture,
            "rainfall_mm": rainfall,
            "rain_rate_mmh": rain_rate
        }

        try:
            response = requests.post(self.endpoint_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            print("Data uploaded successfully:", response.text)
        except requests.exceptions.RequestException as e:
            print("Upload failed:", e)
