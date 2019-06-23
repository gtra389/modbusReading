#!/usr/bin/env python
# 
import minimalmodbus
import time
import urllib3
from time import gmtime, strftime
from urllib.request import urlopen

minimalmodbus.BAUDRATE = 19200
id_No = "6999"

def waterlevReading():    
    # port name, slave address (in decimal)
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    # Register number, number of decimals, function code
    idn = instrument.read_register(1, 0, 3)
    locale = instrument.read_register(0, 0, 3)
    wl = (instrument.read_register(0, 0, 4) -24267)/1000*26.5/18.8    
    print('id='+str(idn))
    print('location='+str(locale))
    print('water level='+str(wl)+' m')
    print('------------------------')
    time.sleep(5)
    return wl

def rainfallReading():    
    # port name, slave address (in decimal)
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 2)
    # Register number, number of decimals, function code
    idn = instrument.read_register(1, 0, 3)
    locale = instrument.read_register(0, 0, 3)
    rf_realVal   = instrument.read_register(0, 0, 4)
    rf_Intensity = instrument.read_register(1, 0, 4)
    print('id='+str(idn))
    print('location='+str(locale))
    print('rainfall='+str(rf_realVal)+' mm')
    print('rainfall='+str(rf_Intensity)+' mm/hr')
    print('------------------------') 
    time.sleep(5)
    return rf_Intensity

while True:
    data1 = waterlevReading()
    data2 = rainfallReading()
    timeQ = strftime("%Y%m%d%H%M%S")
    url = 'http://ec2-54-175-179-28.compute-1.amazonaws.com/update_general.php?site=Mucha&time='+str(timeQ)+'&weather=0&id='+ str(id_No) + \
          '&air=0&acceleration=0&cleavage=0&incline=0&field1='+str(data1)+'&field2='+str(data2)+'&field3=0'
    res = urlopen(url).read()
    print(res)
    print('------------------------')
    time.sleep(30)
