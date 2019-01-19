"""
import onionGpio
import time
import mqtt_functions
import file_manipulation

movementDetectorPin = 8
gpioObj = onionGpio.OnionGpio(movementDetectorPin)
status = gpioObject.setInputDirection()

lastTrigger = ''

def movement():
    if (gpioObj.getValue() == 1):
        timeTrigger = str(int(time.time()/60))
        if (timeTrigger != lastTrigger):
            lastTrigger = timeTrigger
            file_append(movement.txt, lastTrigger)
            dumpMovement(timeTrigger)
"""
import time
from mqtt_functions import*
from file_manipulation import*
import random
import datetime

lastTrigger = ""

def movement():
    global lastTrigger
    now = datetime.datetime.now()
    a = random.randint(1, 10)
    if a > 5:
        timeTrigger = str(now.second)
        if (timeTrigger != lastTrigger):
            lastTrigger = timeTrigger
            file_append("movement.txt", str(now.strftime("%Y-%m-%d %H:%M:%S")))
            dumpMovement(timeTrigger)
            print(timeTrigger)
