#!/usr/bin/python
import paho.mqtt.client as mqttc
import socket
import time

#mqtt_broker = "192.168.0.4"
mqtt_broker = "199.108.99.17"
mqtt_port = 5001
mqtt_client = "Jason-Gew"
mqtt_topic = "jason"

def on_connect(client, obj, flags, rc):
	print "on connect - obj: ", obj
	print "on connect - flags: ", flags
	print rc

	if obj == 0:
		print("First connection:")
	elif obj == 1:
		print("Second connection:")
	elif obj == 2:
		print("Third connection (with clean session=True):")
	print("    Session present: "+str(flags['session present']))
	print("    Connection result: "+str(rc))


def on_disconnect(client, obj, rc):
	print client
	print obj
	print rc
	#client.user_data_set(obj+1)
	if obj == 0:
#		mqttc.reconnect()
		pass
	else:
		pass

def on_publish(client, user_msg, result):
	print("MQTT Publish Success @ {}").format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	print client
	print user_msg
	print result

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(mqttc, obj, msg):
	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


clientj = mqttc.Client(mqtt_client)
clientj.on_connect = on_connect
clientj.on_publish = on_publish
clientj.on_subscribe = on_subscribe
clientj.on_message = on_message

try:
	ct = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	clientj.connect(mqtt_broker,mqtt_port)

	clientj.publish(topic=mqtt_topic, payload="Message from Jason "+ct, retain=False)
#	clientj.subscribe(mqtt_topic, 0)

	clientj.disconnect()
except socket.error, e:
	print "MQTT Publish Fail: ",e
	print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

