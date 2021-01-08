
from mlx90614 import MLX90614
import datetime
from influxdb import InfluxDBClient
import time

thermometer_address = 0x5a

thermometer = MLX90614(thermometer_address)

print(thermometer.get_amb_temp())
print(thermometer.get_obj_temp())

def main():
  tempObj = thermometer.get_obj_temp()
  tempAmb = thermometer.get_amb_temp()

  print("TemperatureSky : ", tempObj, "C")
  print("TemperatureAmb : ", tempAmb, "C")

  mydate = datetime.datetime.utcnow()
  myTime = mydate.strftime('%Y-%m-%dT%H:%M:%SZ')
  print("Zeit ", myTime) 
  json_body = [
  {
    "measurement": "SkyTemp",
      "tags": {
        "location": "Berlin, Tempelhof",
      },
    "time": myTime,
    "fields": {
          "Skytemp": (tempObj),
          "Ambtemp": (tempAmb),
        }
    }
  ]

  client = InfluxDBClient('server adress','port','user','password','database name')
  client.write_points(json_body)


if __name__=="__main__":
   main()       