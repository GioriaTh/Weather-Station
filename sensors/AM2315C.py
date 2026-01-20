import board
import busio
import adafruit_ahtx0

class TempSensor:
    def __init__(self):
        """
        Initializes the AM2315C (AHT20) sensor using the I2C bus.
        """
        try:
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
            # Initialize the sensor
            self.sensor = adafruit_ahtx0.AHTx0(self.i2c)
        except Exception as e:
            print(f"Error initializing AM2315C: {e}")
            self.sensor = None

    def read(self):
        
        if self.sensor is None:
            return {"temperature": 0.0, "humidity": 0.0}

        try:
            temp = self.sensor.temperature
            hum = self.sensor.relative_humidity
            
            # Basic validation to prevent outlier spikes
            if temp is not None and hum is not None:
                return {
                    "temperature": round(temp, 2),
                    "humidity": round(hum, 2)
                }
        except Exception as e:
            print(f"Failed to read from AM2315C: {e}")
            
        return {"temperature": 0.0, "humidity": 0.0}