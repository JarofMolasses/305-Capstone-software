# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:46:06 2021
Python interface for Mech 305 arduino DAQ - live plot and file writing

code is very bad what the heck
@author: Molasses
"""
import serial
from serial import Serial
import serial.tools.list_ports

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('tkAgg')
import matplotlib.animation as animation

import sys
import numpy as np
import pandas as pd

from pathlib import Path
import time
import csv

plt.ion()

#figure storage
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
times = []
pana10 = []
pana25 = []
pana100 = []


ax.plot(times,pana10, 'b-', label = 'Panasonic PM1.0')
ax.plot(times,pana25, 'r-', label = 'Panasonic PM2.5')
ax.set_title("Panasonic sensor readings")
ax.set_ylabel('PM concentration (ug/m3)')
ax.set_xlabel('time (s)')
ax.legend(loc="upper left")
plt.show()

def startup():
    print("----------------------")
    print("Press f to start Serial interface, x to quit")
    startup_select = input("")
    return startup_select

def captureSerial():
    user_input = startup()
    if(user_input == "f" or user_input == "F"):
        port = ""
        print("\nBeginning serial communication")
        liveports = list(serial.tools.list_ports.comports())
        
        for p in liveports:
            print(p)
            
            if "VID:PID=2341:0043" in p.hwid:
                print("Found Arduino looking thing: " + p.description)
                port = p.device
                break
            print("\n")
            
        if(port == ""):
            print("No Arduinos found")
        else:
            print("\nEnter log filename to begin: ")
            csvfile = input("")
            
            ArduinoStream = serial.Serial(port, 115200, timeout=10)
            time.sleep(1)                       #sleep the code for the serial buffer flush
            ArduinoStream.flush()
            time.sleep(1)
            ArduinoStream.close()               #is this how to deal with serial? idk lol but it works reliably
            ArduinoStream.open()
            
            print("\nOpened " + port)
            print("Reading serial: ")
            filename = csvfile + "_" + time.strftime("%Y%m%d_%H-%M-%S") + ".csv"

            lines = 0
            header = 1;
            
            while(lines<100):   #make a gui with a stop button later
            
                while(ArduinoStream.inWaiting() == 0):
                    pass
                
                data = ArduinoStream.readline().decode("utf-8")
                    
                #use split to separate out the data
                datacols = data.split(',')
                
                if(header):
                    print(data)
                    
                else:                              
                    seconds = int(datacols[0])
                    pressure = float(datacols[1])
                    pm10pana = float(datacols[2])
                    pm25pana = float(datacols[3])
                    pm100pana = float(datacols[4])
                    pm10ada = datacols[5]               #need to handle absent sensor detection later
                    pm25ada = datacols[6]
                    pm100ada = datacols[7]
                    

                    times.append(seconds)
                    pana10.append(pm10pana)
                    pana25.append(pm25pana)
                    pana100.append(pm100pana)
                    print(datacols)
                    
                    updatePlot()
                    plt.show()
                    
                with open(logs_folder/ filename, "a") as f:    
                    if(header == 0):
                        f.write(data) 
                    
                if("End of Header" in data):
                    header = 0    
                    
                lines = lines + 1
                
        ArduinoStream.close
        
        return 1
    
    else:
        return 0
    
def updatePlot():
    ax.plot(times,pana10, 'b-', label = 'Panasonic PM1.0')
    ax.plot(times,pana25, 'r-', label = 'Panasonic PM2.5')
    
    plt.pause(0.05)

if __name__ == "__main__":
    logs_folder = Path('logs/')
    logs_folder.mkdir(exist_ok = True)

    captureSerial()
    
    
    
    
    