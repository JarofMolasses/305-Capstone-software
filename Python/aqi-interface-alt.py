# -*- coding: utf-8 -*-
"""
Sandbox: alternate approach using the animation API
@author: Molasses
"""
import serial
from serial import Serial
import serial.tools.list_ports

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('qt4Agg')                        #set graphics backend
from matplotlib import animation  #strictly speaking using this animation API would be much better

import numpy as np
import pandas as pd
 
from pathlib import Path
import time

#global arrays for graphing, initial plot setup
#TODO: use animation API  - maybe pack this up into a class for compactness 
fig = plt.figure('PMplot')
ax = fig.add_subplot(1, 1, 1)
times = []
pana25 = []
lines, = plt.plot([],[], 'ro', label="Panasonic PM2.5")
ax.set_title("Panasonic sensor readings")
ax.set_ylabel('PM concentration (ug/m3)')
ax.set_xlabel('time (s)')
ax.legend(loc="upper left")


logs_folder = Path('logs/')
logs_folder.mkdir(exist_ok = True)

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
else:                                   #main data processing and plot loop
    pass
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
        
ani = animation.FuncAnimation(fig, captureSerial, fargs=(ArduinoStream), frames=300, interval=1000, blit=False)
plt.show()


    
    
    