# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:46:06 2021
Python interface for Mech 305 arduino DAQ - write to logs/[file].csv and real-time plot

code is very bad. dear god
-ineffiicient plt.pause() shreds CPU
@author: Molasses
"""
import serial
from serial import Serial
import serial.tools.list_ports

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('qt4Agg')                     #set graphics backend
#import matplotlib.animation as animation    #strictly speaking using this animation API would be much better

import numpy as np
import pandas as pd
 
from pathlib import Path
import time


plt.close()
plt.ion()

#global arrays for graphing, initial plot setup
#TODO: use animation API  - maybe pack this up into a class for compactness 
fig = plt.figure('PMplot')
ax = fig.add_subplot(1, 1, 1)
times = []
pana10 = []
pana25 = []
pana100 = []
ax.plot(times,pana10, 'r-', label = 'Panasonic PM1.0')
ax.plot(times,pana25, 'g-', label = 'Panasonic PM2.5')
ax.plot(times,pana100, 'b-', label = 'Panasonic PM10')
ax.set_title("Panasonic sensor readings")
ax.set_ylabel('PM concentration (ug/m3)')
ax.set_xlabel('time (s)')
ax.legend(loc="upper left")


def startup():              #unused sort of mode-select function
    print("----------------------")
    print("Press f to start Serial interface, x to quit")
    startup_select = input("")
    return startup_select


def main():                 #main program
    port = ""
    print("\nBeginning serial communication")
    liveports = list(serial.tools.list_ports.comports())
    
    
    #automatically scan for Arduino VID:PID
    for p in liveports:
        print(p)
        if "VID:PID=2341:0043" in p.hwid:
            print("Found Arduino looking thing: " + p.description)
            port = p.device
            break
        print("\n")
        
        
    if(port == ""):
        print("No Arduinos found, exiting.")
        return 1
    else:                                   #main data processing and plot loop
        print("\nEnter log file name to begin: ")
        csvfile = input("")
        
        ArduinoStream = serial.Serial(port, 115200, timeout=10)
        
        ArduinoStream.flush()
        time.sleep(0.5)                     #sleep the code for a moment, for the serial buffer flush
        ArduinoStream.close()               #is this how to deal with serial? idk lol but it works reliably
        ArduinoStream.open()
        
        print("\nOpened " + port)
        print("Reading serial: ")
        filename = csvfile + "_" + time.strftime("%Y%m%d_%H-%M-%S") + ".csv"

        lines = 0         
        header = 1;
        while(lines<300):   #TODO: replace with animation api (lines~frames), and add gui with interrupt
            header = captureSerial(ArduinoStream, filename, header)
            lines += 1
            
    ArduinoStream.close
    
    print("\n\nWell, the moment has passed. Back to work")
    return 1
    

def captureSerial(ArduinoStream, filename, header):
    newheader = header;
    while(ArduinoStream.inWaiting() == 0):              #wait here if the serial buffer is empty
        pass
            
    data = ArduinoStream.readline().decode("utf-8")     #read line from serial in and strip out the utf-8 bits
    datacols = data.split(',')                          #use split to separate out the data columns
    
    if(newheader):
        print(data)
    else:                                   #extracting out all of the data, clumsily       
        print(datacols)    
        try:
            seconds = int(datacols[0])
            pressure = float(datacols[1])
        
            pm10pana = float(datacols[2])
            pm25pana = float(datacols[3])
            pm100pana = float(datacols[4])
        
            pm10ada = datacols[5]               #TODO: adafruit sensor, and still need to handle absent sensor detection
            pm25ada = datacols[6]
            pm100ada = datacols[7]
        
            times.append(seconds)               #append data to global panasonic arrays 
            pana10.append(pm10pana)
            pana25.append(pm25pana)
            pana100.append(pm100pana)
      
            updatePlot()
        except:
            pass    
        
    with open(logs_folder/ filename, "a") as f:    
        if(header == 0):
            f.write(data) 
        
    if("End of Header" in data):        #update header flag when we reach end of the header
        newheader = 0    
    
    return newheader;                   #return new header flag to main


def updatePlot():                               #redraw the plot. clumsy: you have to make sure to plot in the same colors that were initialized at the beginning
    ax.plot(times,pana10, 'r-')
    ax.plot(times,pana25, 'g-')
    ax.plot(times,pana100, 'b-')
    
    plt.pause(0.001)                           #crude animation.


if __name__ == "__main__":
    logs_folder = Path('logs/')
    logs_folder.mkdir(exist_ok = True)

    main()

    
    
    
    
    