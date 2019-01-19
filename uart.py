import random

def getTemp():
	return random.randint(1, 10)
def getHumid():
	return random.randint(1, 10)
def getLightning():
	return random.randint(1, 10)
"""
import serial

port = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=3.0)

def getTemp()
	port.write(1)
	return port.read(20)
def getHumid()
	port.write(1)
	return port.read(20)
def getLightning()
	port.write(1)
	return port.read(20)
"""
