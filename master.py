import paho.mqtt.client as mqtt
import re
from chauvenet import*
from file_manipulation import*
from mqtt_functions import*
import datetime
import time


room = "1f04"
topic_names = [room+"/slave/+/temp", room+"/slave/+/humid", room+"/slave/+/lightning", room+"/slave/+/movement", room+"/master/light"]
broker = "test.mosquitto.org"
temp = []
last_temp = []
humid = []
last_humid = []
lightning = []
last_lightning = []
movement = ''
light = 0

def on_connect(client, userdata, flags, rc):
    for topic in topic_names:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    if(re.compile('temp').search(msg.topic)):
        temp.append(float(msg.payload.decode()))
    if(re.compile('humid').search(msg.topic)):
        humid.append(float(msg.payload.decode()))
    if(re.compile('lightning').search(msg.topic)):
        lightning.append(float(msg.payload.decode()))
    if(re.compile('movement').search(msg.topic)):
        print(msg.payload.decode())

mqttc = mqtt.Client()
mqttc.connect(broker, 1883, 60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_start()

while True:
    now = datetime.datetime.now()
    time.sleep(1)
    if len(temp) != 0:
        Temp = prep_cleanup(temp)
        file_append("room_Temp.txt", str(Temp) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        temp = list(set(temp).symmetric_difference(set(last_temp)))
        last_temp = temp

    if len(humid) != 0:
        Humid = prep_cleanup(humid)
        file_append("room_Humid.txt", str(Humid) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        humid = list(set(humid).symmetric_difference(set(last_humid)))
        last_humid = humid
        
    if len(lightning) != 0:
        Lightning = prep_cleanup(lightning)
        file_append("room_Lightning.txt", str(Lightning) + " " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
        lightning = list(set(lightning).symmetric_difference(set(last_lightning)))
        last_lightning = lightning



    """
    if movement != last_movement:
        last_movement = movement
        file_append("room_movement.txt", movement)
    """

    """    
    if humid:
        Humid = prep_cleanup(humid)
        file_append("room_Humid.txt", Humid)
    if lightning:
        Lightning = prep_cleanup(lightning)
        file_append("room_Lightning.txt", Lightning)
    
    setLight(light)
    """
mqttc.loop_stop()
