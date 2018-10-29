import paho.mqtt.client as mqtt
import socket


broker = "test.mosquitto.org"
room = "1f04"


#For the slaves
#Dumping

def dumpTemp(temp):	#imput string
	topicName = room+"/slave/"+socket.gethostname()+"/temp"
	mqttc = mqtt.Client()
	mqttc.connect(broker)
	message = temp
	mqttc.publish(topicName, message)

def dumpHumid(humid):	#imput string
	topicName = room+"/slave/"+socket.gethostname()+"/humid"
	mqttc = mqtt.Client()
	mqttc.connect(broker)
	message = humid
	mqttc.publish(topicName, message)

def dumpLightning(stat):	#imput string
	topicName = room+"/slave/"+socket.gethostname()+"/lightning"
	mqttc = mqtt.Client()
	mqttc.connect(broker)
	message = stat
	mqttc.publish(topicName, message)

def dumpMovement(mov):
	topicName = room+"/slave/"+socket.gethostname()+"/movement"
	mqttc = mqtt.Client()
	mqttc.connect(broker)
	message = mov
	mqttc.publish(topicName, message)

#Retrieving

#For the master
#Dumping

def setLightning(stat):	#send light percentage
	topicName = room+"/master/light"
	mqttc = mqtt.Client()
	mqttc.connect(broker)
	message = humid
	mqttc.publish(topicName, message)

#Retrieving
