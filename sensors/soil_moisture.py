import spidev

class SoilSensor:
    def __init__(self, bus=0, device=0, channel=0):
      
        self.channel = channel
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1350000 # Standard for MCP3008
        
        # Calibration Values: Adjust these based on your specific sensor
        # 'air_value' is the reading when completely dry
        # 'water_value' is the reading when submerged in water
        self.air_value = 1023   
        self.water_value = 312 

    def _read_raw(self):
        """Reads raw data from the MCP3008."""
        # MCP3008 protocol: Start bit, Single-ended bit, Channel bits
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def read(self):
        """
        Calculates moisture percentage.
        :return: Dictionary containing raw value and moisture percent.
        """
        raw_val = self._read_raw()
        
        # Map the raw value to 0-100%
        # Note: Capacitive sensors usually have LOWER values when WETTER
        moisture_percent = ((self.air_value - raw_val) / (self.air_value - self.water_value)) * 100
        
        # Constrain between 0 and 100
        moisture_percent = max(0, min(100, round(moisture_percent, 2)))
        
        return {
            "raw_adc": raw_val,
            "moisture_percent": moisture_percent
        }

    def close(self):
        """Closes the SPI connection."""
        self.spi.close()