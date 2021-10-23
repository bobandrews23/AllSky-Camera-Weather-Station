# AllSky Camera Weather Station
 An Allsky Camera based on a Raspi4 with Weather, Cloud Detector and Light Measurement
This case is built for a ASI 120 and other cameras that use the same body. 
The allsky software is from Thomas Jacquin:
https://github.com/thomasjacquin/allsky

The case is made in TinkerCad. It's public so you can duplicate it, mod it to your needs or just pull the .stl’s for your printer.
https://www.tinkercad.com/things/eZ6Q4UBwBwD



-------------------------------
IR Clouds Sensor is a mlx90614 without a lens. It is installed on the backside of the top casing. I used a piece of cling warp to waterproof it and designed a clip on holder for it. The FoV works quite good. A test run can be seen here:
https://www.youtube.com/watch?v=U40YY0d422w

mlx90614 i2c address is 0x5a

Call the class script and then readout the values. Two values can be acquired, sky temperature and sensor temperatur. The sensor temperature can either be used to calibrate the sky temp or, as I use it, as an internal temp probe for the casing. 



-------------------------------
The weather data is acquired from two bme280 sensors. One in the outside housing, the other for control purpose inside the case. Both sensors will have the same i2c address. In order to use both, you will need to modify one of them by shortening a solder jumper. 
https://lastminuteengineers.com/bme280-arduino-tutorial/

The i2c addresses will be 0x76 and 0x77



-------------------------------
I also read out the temp and sky values, calculate a dewpoint and write that into a text file, which then can be used to overlay the additional data with the Thomas Jacquin software.

All scripts are run through a cron job. all in Python 3

bme280_v2.py reads the sensors, prints the data to the terminal and exports it as json to an Influx database. 

sensorcall.py does the same, but writes the data into a text file called Data.txt



-------------------------------
I have some code in there (deactivated) when I tried to utilize the tsl2591 as a SQM meter, but that doesn’t seem to work. This sensor is not sensitive enough for long exposures. I never got measurements beyond 16 mag/arcs . 
You can find more info about that here:
https://sourceforge.net/projects/mysqmproesp32/ 

or, if you fit in c++, here is a project with proper calibration of the TSL2591.
https://github.com/gshau/SQM_TSL2591
Unfortunately I can only stumble around with python, so this is still waiting for me to work on. 

![Bildschirmfoto 2021-01-08 um 08 20 42](https://user-images.githubusercontent.com/66861958/103986112-75493200-518a-11eb-89cf-feeac8c95ad7.jpg)



