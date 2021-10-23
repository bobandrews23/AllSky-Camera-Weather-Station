#!/usr/bin/python3

import datetime
import board
import digitalio
import busio
import time
import adafruit_bme280
import math
from influxdb import InfluxDBClient
from mlx90614 import MLX90614

# Default device I2C address for IR
IR_thermometer_address = 0x5a


thermometer = MLX90614(IR_thermometer_address)
#read and define IR measurements
tempObj = thermometer.get_obj_temp()
tempIRAmb = thermometer.get_amb_temp()


# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#or with other sensor address
bme280amb = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280enc = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

# change this to match the location's pressure (hPa) at sea level
bme280amb.sea_level_pressure = 1013.25

#line to adjust the measurements by adding or subtracting last value
pressureCorrAmb = (bme280amb.pressure + 0)
humidityCorrAmb = (bme280amb.humidity + 0)
tempertureCorrAmb = (bme280amb.temperature - 0)

#dewpoint calculation
b = 17.62
c = 243.12
gamma = (b * tempertureCorrAmb / (c + tempertureCorrAmb)) + math.log(humidityCorrAmb / 100.0)
dewpointAmb = (c * gamma) / (b - gamma)
deltaDew = (tempertureCorrAmb - dewpointAmb)

#print values
print("\nDewpoint Ambient: %0.1f C" % dewpointAmb)
print("Temperature: %0.1f C" % tempertureCorrAmb)
print("Humidity Ambient: %0.1f %%" % humidityCorrAmb)
print("Pressure Ambient: %0.1f hPa" % pressureCorrAmb)
print("Altitude = %0.2f meters" % bme280amb.altitude)
print("Delta Dewpoint = %0.1f C" % deltaDew)
print("Temperature IR sensor: %0.1f C" % tempIRAmb)
print("Temperature Enclosure: %0.1f C" % bme280enc.temperature)
print("Humidity Enclosure: %0.1f %%" % bme280enc.humidity)
print("Pressure Enclosure: %0.1f hPa" % bme280enc.pressure)
time.sleep(2)

#do some date/time calculations for Influx entries
mydate = datetime.datetime.utcnow()
myTime = mydate.strftime('%Y-%m-%dT%H:%M:%SZ')
print("Zeit ", myTime)

#create json body for database entries
json_body = [
  {
    "measurement": "bme280",
      "tags": {
        "location": "Suderburg, Lower Saxony, DE",
      },
    "time": myTime,
    "fields": {
          "temp": (float(tempertureCorrAmb)),
          "dew": (float(dewpointAmb)),
          "press": (float(pressureCorrAmb)),
          "hum": (float(humidityCorrAmb)),
          }
    },
   {
    "measurement": "bme280enclosure",
      "tags": {
        "location": "Berlin, Tempelhof",
      },
    "time": myTime,
    "fields": {
          "temp": float(bme280enc.temperature),
          "press": float(bme280enc.humidity),
          "hum": float(bme280enc.pressure)
        }
    }  
]



#connect to influxDB and write data

client = InfluxDBClient('server adress','port','user','pass','db_name')
client.write_points(json_body)

