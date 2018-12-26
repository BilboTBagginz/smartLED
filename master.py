import paho.mqtt.client as mqtt
import re
import chauvenet
import file_manipulation
import mqtt_functions


room = "1f04"
topic_names = [room+"/slave/+/temp", room+"/slave/+/humid", room+"/slave/+/lightning", room+"/slave/+/movement", room+"/master/light"]
broker = "mosquitto.org"
temp = []
humid = []
lightning = []
movement= ''
last_movement=''
light= 0

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

mqttc = mqtt.Client()
mqttc.connect(broker, 1883, 60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_forever()

while 1
    if movement != last_movement:
        last_movement = movement
            file_append(room_movement.txt, movement)

    Temp = prep_cleanup(temp)
    file_append(room_Temp.txt, Temp)
    Hymid = prep_cleanup(humid)
    Humidfile_append(room_Humid.txt, Humid)
    Lightning = prep_cleanup(lightning)
    file_append(room_Lightning.txt, Lightning)

    if Humid < 0.8



    setLight(light)