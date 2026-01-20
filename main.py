import time
import os
import cv2
from datetime import datetime

from sensors.AM2315C import TempSensor
from sensors.DFRobot_RainfallSensor import DFRobot_RainfallSensor_I2C
from sensors.soil_moisture import SoilSensor
from sensors.camera import USBCamera

from storage.google_drive import GoogleDriveUploader
from storage.json_upload import JSONUploader

def main():
    am2315 = TempSensor()
    rain = DFRobot_RainfallSensor_I2C(1)
    soil = SoilSensor(channel=0)
    camera = USBCamera()

    drive = GoogleDriveUploader()
    json_uploader = JSONUploader(
        endpoint_url="http://gioria.netsire.gr/db_costa.php"
    )

    # --- NEW: Initialize tracking variables ---
    rain_baseline = rain.get_rainfall()  # mm (raw accumulated)
    period_start_rain = 0.0
    period_start_time = time.time()

    last_reset_day = datetime.now().day
    last_capture_day = None

    print("Weather station started")
    print(f"Initial rain baseline: {rain_baseline:.1f} mm")
    
    
    try:
        while True:
            now = datetime.now()

            # 1. HARD RESET: Midnight Reset (Daily Total back to 0)
            if now.day != last_reset_day:
                print(f"[{now}] Midnight detected → daily rain reset")
                rain_baseline = rain.get_rainfall()
                period_start_rain = 0.0
                last_reset_day = now.day


            # 2. Read Sensors
            am2315_data = am2315.read()
            soil_data = soil.read()
            
            raw_rain = rain.get_rainfall()
            daily_rain = max(0.0, raw_rain - rain_baseline)

            current_time = time.time()

            # ---------- RAIN INTENSITY ----------
            delta_rain = daily_rain - period_start_rain
            delta_hours = (current_time - period_start_time) / 3600.0

            if delta_hours > 0 and 0 <= delta_rain <= 5:
                avg_rain_rate = delta_rain / delta_hours
            else:
                avg_rain_rate = 0.0

            print(
                f"[{now}] "
                f"Temp: {am2315_data['temperature']:.2f} °C | "
                f"Hum: {am2315_data['humidity']:.2f} % | "
                f"Daily Rain: {daily_rain:.1f} mm | "
                f"Avg Rate: {avg_rain_rate:.2f} mm/h | "
                f"Soil: {soil_data['moisture_percent']} %"
            )

            # 4. Upload Data
            json_uploader.upload_measurement(
                timestamp=str(datetime.now()),
                temperature=am2315_data["temperature"],
                humidity=am2315_data["humidity"],
                soil_moisture=soil_data["moisture_percent"],
                rainfall=daily_rain, # Sends the daily total
                rain_rate=avg_rain_rate    # Sends the calculated intensity
            )

            # 5. SOFT RESET: Set baseline for the NEXT 10 minutes
            period_start_rain = daily_rain
            period_start_time = current_time

            # 6. Daily photo logic
            if now.day != last_capture_day:
                img = camera.capture_image()
                if img is not None:
                    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                    local_filename = f"capture_{timestamp}.jpg"
                    cv2.imwrite(local_filename, img)
                    try:
                        drive.upload(local_filename, local_filename)
                        last_capture_day = now.day
                        os.remove(local_filename)
                    except Exception as e:
                        print(f"Drive upload failed: {e}")
                else:
                    print("Failed to capture image from camera")
               
            # Sleep until next upload
            time.sleep(30)  # 10 minutes

    except KeyboardInterrupt:
        print("\nStopping weather station...")

    finally:
        soil.close()
        print("SPI closed cleanly")

if __name__ == "__main__":
    main()