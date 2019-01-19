from uart import*
import time
from mqtt_functions import*
import paho.mqtt.client as mqtt
from file_manipulation import*
from movement import*

done = 0
room = "1f04"
topic_light = room+"/master/light"
broker = "test.mosquitto.org"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_light)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

lastTrigger = ''

while 1:
    time.sleep(1)
    now = datetime.datetime.now()
    tim = int(round(time.time()))
    last_time = 0

    if (tim % 5 == 0) and (tim != last_time) and not done:
        last_time = tim
        done = 1

        temp = getTemp()
        dumpTemp(temp)
        file_append("temp.txt", str(temp) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        humid = getHumid()
        dumpHumid(humid)
        file_append("humid.txt", str(humid) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        lightning = getLightning()
        dumpLightning(lightning)
        file_append("lightning.txt", str(lightning) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        

    elif (tim % 5 != 0):
        done = 0
    movement()

client.loop_stop()
