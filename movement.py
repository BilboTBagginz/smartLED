import onionGpio
import time

movementDetectorPin = 8
gpioObj = onionGpio.OnionGpio(movementDetectorPin)
status = gpioObject.setInputDirection()

lastTrigger = ''

def movement():
    if (gpioObj.getValue() == 1):
        timeTrigger = str(int(time.time()/60))
        if (timeTrigger != lastTrigger):
            lastTrigger = timeTrigger
            dumpMovement(timeTrigger)
