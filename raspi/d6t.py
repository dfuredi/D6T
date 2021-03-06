#! /usr/bin/python

# A simple Python command line tool to control an Omron MEMS Temp Sensor D6T-44L
# By Greg Griffes http://yottametric.com
# GNU GPL V3 

# Jan 2015
from __future__ import print_function

import smbus
import sys
import getopt
from datetime import datetime 
import time
import pigpio

i2c_bus = smbus.SMBus(1)
OMRON_1=0x0a          # 7 bit I2C address of Omron MEMS Temp Sensor D6T-44L
OMRON_BUFFER_LENGTH=35        # Omron data buffer size
temperature_data=[0]*OMRON_BUFFER_LENGTH  # initialize the temperature data list
tdata=[0]*17;

# intialize the pigpio library and socket connection to the daemon (pigpiod)
pi = pigpio.pi()              # use defaults
version = 'Version'+str(pi.get_pigpio_version())
print(version)
handle = pi.i2c_open(1, 0x0a) # open Omron D6T device at address 0x0a on bus 1

while True:
    
    sys.stdout.write( "%s;" % str(datetime.now()))

    # initialize the device based on Omron's appnote 1
    result=i2c_bus.write_byte(OMRON_1,0x4c);
    #print 'write result = '+str(result)

    #for x in range(0, len(temperature_data)):
       #print x
       # Read all data  tem
       #temperature_data[x]=i2c_bus.read_byte(OMRON_1)
    (bytes_read, temperature_data) = pi.i2c_read_device(handle, len(temperature_data))
    #print('Bytes read from Omron D6T: '+str(bytes_read))
    sys.stdout.write("%s;" % bytes_read)
    
    ptat = (temperature_data[0]+256*temperature_data[1])*0.1; # reference Temp
    # Display data 
    #print('Reference data : '+str(ptat))  
    #print('Data read from Omron D6T : ')
    #for i in range(bytes_read):
    #  sys.stdout.write("%s;" % temperature_data[i])

    for i in range(17):
    #  print(i),  
      tdata[i] = (temperature_data[(i*2)]+256*temperature_data[(i*2+1)])*0.1;
      sys.stdout.write("%s;" % tdata[i])
    print('')
    time.sleep(1)

