import paho.mqtt.client as mqtt
import re

room = "1f04"
topic_names = [room+"/slave/+/temp", room+"/slave/+/humid", room+"/slave/+/lightning", room+"/slave/+/movement", room+"/master/light"]
broker = "mosquitto.org"
temp = []
humid = []
lightning = []

def on_connect(client, userdata, flags, rc):
    for topic in topic_names:
        client.subscribe(topic)

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
