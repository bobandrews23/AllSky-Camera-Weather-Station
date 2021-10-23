#!/usr/bin/python3
import sys
import smbus
import time
import datetime
import board
import busio
import digitalio
import math
import adafruit_bme280
from mlx90614 import MLX90614
import adafruit_tsl2591

########### start SQM Lux #################
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
 
# Initialize the sensor.
#sensor = adafruit_tsl2591.TSL2591(i2c)
 
# You can optionally change the gain and integration time:
# sensor.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
# sensor.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
# sensor.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
# sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms, default)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)
 
# Read and calculate the light level in lux.
##lux = sensor.lux
#print("Total light: {0}lux".format(lux))
# You can also read the raw infrared and visible light levels.
# These are unsigned, the higher the number the more light of that type.
# There are no units like lux.
# Infrared levels range from 0-65535 (16-bit)
##infrared = sensor.infrared
#print("Infrared light: {0}".format(infrared))
# Visible-only levels range from 0-2147483647 (32-bit)
##visible = sensor.visible
#print("Visible light: {0}".format(visible))
# Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
##full_spectrum = sensor.full_spectrum
#print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
##time.sleep(1.0)

##def Lux_to_SQM(lux):
##   return 15.2-math.log(lux)/math.log(2.5)

##SQM = Lux_to_SQM(lux)
##print("Lux: %f" %lux)
##print("SQM: %f" %SQM)

########### end SQM Lux #################


# Default device I2C address for IR
IR_thermometer_address = 0x5a

thermometer = MLX90614(IR_thermometer_address)
#read and define IR measurements
tempObj = thermometer.get_obj_temp()
tempAmb = thermometer.get_amb_temp()

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
#or with other sensor address
bme280amb = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280enc = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x77)

# change this to match the location's pressure (hPa) at sea level
bme280amb.sea_level_pressure = 1013.25

#line to adjust the pressure by adding or subtracting last value
pressureCorrAmb = (bme280amb.pressure + 0)
humidityCorrAmb = (bme280amb.humidity + 0)
#pressureCorrEnc = (bme280amb.pressure + 0)
humidityCorrEnc = (bme280enc.humidity + 0)
tempertureCorrEnc = (bme280enc.temperature - 0)

#dewpoint calculation
b = 17.62
c = 243.12
gamma = (b * bme280amb.temperature /(c + bme280amb.temperature)) + math.log(humidityCorrAmb / 100.0)
dewpointAmb = (c * gamma) / (b - gamma)
#gamma = (b * tempertureCorrEnc /(c + tempertureCorrEnc)) + math.log(humidityCorrEnc / 100.0)
#dewpointEnc = (c * gamma) / (b - gamma)

#output values for testing

#print("\nFull Spectrum (IR + Visible) :%f lux" %full_spectrum)
#print("Infrared Value :%0.1f lux" %infrared)
#print("Visible Value :%0.1f lux" %visible)
#print("SQM mag/arsecond:", SQM)
print("\n")
print("Sky Temperature: %0.1f C" % tempObj)

print("\nDewpoint Ambient: %0.1f C" % dewpointAmb)
print("Temperature: %0.1f C" % bme280amb.temperature)
print("Humidity Ambient: %0.1f %%" % humidityCorrAmb)
print("Pressure Ambient: %0.1f hPa" % pressureCorrAmb)
#print("Altitude = %0.2f meters" % bme280amb.altitude)
print("Altitude = 79 meters")
#print("\nDewpoint Enclosure: %0.1f C" % dewpointEnc)
print("Temperature IR Sensor: %0.1f C" % tempAmb)
print("Temperature Enclosure: %0.1f C" % bme280enc.temperature)
print("Humidity Enclosure: %0.1f %%" % humidityCorrEnc)
time.sleep(2)

  
#write (and overwrite in next call) to file Data.txt  
file1 = open("Data.txt","w")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write("\n")
file1.write(str(round(pressureCorrAmb, 2)) + " hPa" "\n")
#file1.write("Pressure \n")
file1.write("\n")
file1.write("Ambient \n")
file1.write(str(round(bme280amb.temperature, 1)) + " C" "\n")
file1.write(str(round(humidityCorrAmb, 1)) + " %" "\n")
file1.write(str(round(dewpointAmb, 1)) + " C dewpoint" "\n")
file1.write("\n")
file1.write("Enclosure \n")
file1.write(str(format(tempAmb, '.1f')) + " C IRsensor" "\n")
file1.write(str(round(tempertureCorrEnc,1 )) + " C InstrumentArray" "\n")
file1.write(str(round(humidityCorrEnc, 1)) + " % Hum" "\n")
file1.write("\n")
file1.write("ENVIRONMENTAL DATA: \n")
file1.write(str(round(tempObj, 1)) + " C Skytemp" "\n")
#file1.write(str(visible) + " Lux Visible" "\n")
#file1.write(str(round(SQM, 2)) + " mag/arsecond" "\n")
#file1.write("Pressure \n")
file1.close()
