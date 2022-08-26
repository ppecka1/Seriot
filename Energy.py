#!/usr/bin/python3
# -*- coding: utf8 -*-

#import csv
import serial
import time
import struct
import socket
#import matplotlib.pyplot as plt
#import pandas as pd


# portName = 'COM5'     # for windows users
# portName = '/dev/ttyUSB0'


class Energy():
    def __init__(self):
        portName = '/dev/ttyACM0'
        baudRate = 115200
        ACS712_05_Sens = 0.185 # czulosc czujnika pradowego NIE UZYWANE
        print('Trying to connect to: ' + str(portName) + ' at ' + str(baudRate) + ' BAUD.')
        try:
            self.ser = serial.Serial(portName, baudRate, timeout=2)
            print('Connected to ' + str(portName) + ' at ' + str(baudRate) + ' BAUD.')
        except Exception as e:
            print("Failed to connect with " + str(portName) + ' at ' + str(baudRate) + ' BAUD.')
            print(type(e))    # the exception instance
            print(e.args)     # arguments stored in .args
            print(e)
            exit(-1)
        print ('Device Reset')
        # wyzeruj urzadzenie
        self.ser.flushInput()
        self.ser.write(str.encode('z'))
        time.sleep(1)
    def getEnergy(self):
        self.ser.flushInput()
        self.ser.write(str.encode('a'))
    #print('moc uśredniona - string')
        powerstr = self.ser.readline().decode('utf-8') # format: 'power=17.966 W'
        powerstr=powerstr.split('=')
        powerstr=powerstr[1].split(' ')
        return float(powerstr[0])
    #def __del__(self):
    #   self.ser.close()
#Test:
#print(socket.gethostname())
#ene=Energy()
#for i in range(0,5):
#    print(ene.getEnergy())
    

"""
#odczytaj dane o mocy uśrednionej jako 4 bajty zmiennej float
ser.flushInput()
rawData = bytearray(4)
ser.write(str.encode('A'))
ser.readinto(rawData)
powerbin, = struct.unpack('<f', rawData)  # use 'f' for a 4 byte float
print('moc uśredniona - binarnie (4 bytes float)')
print(powerbin)
print('\r\n')
"""






