import uart
import time
import mqtt_functions
import movement
import pyonionlight
import file_manipulation

done = 0

topic_light = room+"/master/light"
broker = "mosquitto.org"

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic_light)

def on_message(client, userdata, msg):
    if(re.compile('temp').search(msg.topic)):
        temp.append(msg.payload.decode())
    if(re.compile('humid').search(msg.topic)):
        humid.append(msg.payload.decode())
    if(re.compile('lightning').search(msg.topic)):
        lightning.append(msg.payload.decode())
    if(re.compile('movement').search(msg.topic)):
        print(msg.payload.decode())
    if(re.compile('light').search(msg.topic)):
        print(msg.payload.decode())

mqttc = mqtt.Client()
mqttc.connect(broker, 1883, 60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_forever()

while 1:

    tim = int(round(time.time()))
    last_time = 0

    if (tim % 5 == 0) and (tim != last_time) and not done:
        last_time = tim
        done = 1

        temp = getTemp()
        dumpTemp(temp)
        file_append(temp.txt, temp)
        humid = getHumid()
        dumpHumid(humid)
        file_append(humid.txt, humid)
        ligntning = getLightning()
        dumpLightning(lightning)
        file_append(lightning.txt, lightning)
        

    elif (tim % 5 != 0):
        done = 0

    movement()
    