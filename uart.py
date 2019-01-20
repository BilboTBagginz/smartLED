"""
import serial
import time
import random


def getTemp():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b't')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def getHumid():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b'h')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def getLightning():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b'l')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def getBlt():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b'b')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def getIr():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b'i')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def getMovement():
	port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
	port.write(b'm')
	time.sleep(0.05)
	return(int(hex(ord(port.read(8))), 16))

def setLight(light):
	if light * 2000 < 500:
		port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
		port.write(b'X')
	if light * 2000 < 1000:
		port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
		port.write(b'Y')
	else:
		port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)
		port.write(b'Z')
"""
import random
import os

def getTemp():

	return(random.randint(0, 100))

def getHumid():

	return(random.randint(0, 100))

def getLightning():

	return(random.randint(0, 100))

def getBlt():

	return(random.randint(0, 1))

def getIr():

	return(random.randint(0, 1))

def getMovement():

	return((random.randint(0, 1)))
"""
def setLight(light):
	print(light)
"""
def setLight(light):
	pwm = "fast-gpio pwm 3 100 " + light
	os.system(pwm)
