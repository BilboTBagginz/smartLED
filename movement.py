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
