import paho.mqtt.client as mqtt
import socket

#For the slaves
#Dumping

def dumpTemp(temp):	#imput string
	topicName = "room/slave/"+socket.gethostname()+"/temp";
	mqttc = mqtt.Client();
	mqttc.connect("test.mosquitto.org");
	message = temp;
	mqttc.publish(topicName, message);

def dumpHumid(humid):	#imput string
	topicName = "room/slave/"+socket.gethostname()+"/humid";
	mqttc = mqtt.Client();
	mqttc.connect("test.mosquitto.org");
	message = humid;
	mqttc.publish(topicName, message);

#Retrieving

#For the master
#Dumping

def setLightning(stat):	#send light percentage
	topicName = "room/master/light";
	mqttc = mqtt.Client();
	mqttc.connect("test.mosquitto.org");
	message = humid;
	mqttc.publish(topicName, message);

#Retrieving