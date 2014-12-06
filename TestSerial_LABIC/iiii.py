# -*- coding: utf-8 -*-

import serial
import time

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("/dev/ttyAMA0", baudrate=4800, timeout=1.0)

if (ser.isOpen() == False):
	ser.open()
	print('port open')

