#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MQTT Based PubSub Asynchronous Client
# This basic application supports MQTT Publish and Subscribe + Queue.
# The advanced verion App in not open source, but supports End-2-End encryption(AES, PGP), Message log in MySQL, access control, etc
#
# Produced By Jason/Ge Wu
# Current Release on Feb/20/2017

import paho.mqtt.client as mqtt
from Queue import Queue
import threading
import datetime
import logging
import socket
import time

#######  Global Variable  #######
log_path = "client.log"

mqtt_broker = "iot.eclipse.org"
mqtt_port = 1883

mqtt_keepalive = 120

pub_topic = "test001"
sub_topic = "test001"

thread1_status = False
thread2_status = False
thread3_status = False

#################################


########  System Log  ########
def basic_log(level, message):
	global log_path
	'''
	%(module)s : invoked module
	%(funcName)s : invoked function
	%(lineno)d : invoked function line number
	%(thread)d : thread ID (May not have)
	%(threadName)s : thread name (May not have)
	%(process)d : process ID (May not have)
	'''
	logging.basicConfig(level = logging.INFO,  # Reset log print level if necesary
						format = '[%(asctime)s] %(levelname)s: %(message)s',  
						datefmt = '%Y-%m-%d %H:%M:%S',  
						filename = log_path,  
						filemode ='a' # 'a' = append, 'w' = overwrite
						)  
	if level == 'debug' or level == 'Debug' or level == 'DEBUG':
		logging.debug(message)
	elif level == 'info' or level == 'Info' or level == 'INFO':
		logging.info(message)
	elif level == 'warning' or level == 'Warning' or level == 'WARNING':
		logging.warning(message)
	elif level ==  'error' or level == 'Error' or level == 'ERROR':
		logging.error(message)
	elif level == 'critical' or level == 'Critical' or level == 'CRITICAL':
		logging.critical(message)
	else:
		logging.info('Unidentify:'+message)


########  MQTT Extension Functions  ########
def on_connect(mqttc, obj, flags, rc):
	# 0: Connection success 1: Connection refused - incorrect protocol version 2: Connection refused - invalid client identifier 
	# 3: Connection refused - server unavailable 4: Connection refused - bad username or password 5: Connection refused - not authorised
	print("-> MQTT Connection Result Code: "+str(rc))
	if rc == 0:
		print("-> Connection Success")
	elif rc == 1:
		print("-> Connection Refused: Incorrect Protocol Version")
	elif rc == 2:
		print("-> Connection Refused: Invalid Client Identifier")
	elif rc == 3:
		print("-> Connection Refused: Server Unavailable")
	elif rc == 4:
		print("-> Connection Refused: Bad Username or Password")
	else:
		print("-> Unknown Error")


def on_publish(mqttc, obj, mid):
	current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	print("[{}] Message ID:{}").format(current_time, str(mid))

def on_message(mqttc, userdata, message):
	print("Message Received: "+str(message.payload.decode("utf-8")))
	msg_queue.put(str(message.payload.decode("utf-8")))

def on_disconnect(mqttc, userdata, rc):
	print ("-> Disconnected from MQTT Broker with Code: {}").format(rc)
	while rc != 0:
		print ("-> Reconnecting to MQTT Broker...")
		try:
			rc = reconnect()
		except socket.error, e:
			print(e[1])
			self.rc = rc


### Thread-1: MQTT Node Message Subscribe to Queue ###
class node_message(threading.Thread):

	msg_size_limit = 1000
	user_quit = ["\q", "\Q", "\quit", "\Quit", "\exit"]

	def __init__(self, thread_name, msg_queue, mqttc):
		threading.Thread.__init__(self, name = thread_name)
		self.msg = msg_queue
		self.mqttc = mqttc

	def pre_check(self, user_msg):
		status = 0

		if len(user_msg) > self.msg_size_limit:
			print("-> Message Size Beyond the Maximum [{}]\n-> [{}] Overload").format(self.msg_size_limit, len(user_msg)-self.msg_size_limit)
			status = 0

		elif user_msg == "" or user_msg.isspace():
			print("-> Empty Payload")
			status = 0

		elif user_msg in self.user_quit:
			print("-> User Terminate...")
			status = -1

		else:
			status = 1

		return status


	def run(self):
		global thread1_status, pub_topic
		while True:
			thread1_status = True
			try:

				user_msg = raw_input("")
				check = self.pre_check(user_msg)
				if check == -1:
					self.mqttc.disconnect()
					self.mqttc.loop_stop()
					thread1_status = False
					break

				elif check == 0:
					print("-> Please Re-enter the Message:\n")
					pass

				elif check == 1:
					try:
						self.mqttc.publish(pub_topic, user_msg)
						print("You Send: {}").format(user_msg)
					except:
						print("-> MQTT Publish Failed!")

				else:
	 				pass

			except Exception as err:
				print("{} Thread-1: {}").format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.getName())
				print("-> Exception Error: ", err)
				basic_log("Error", "Thread-1 Terminated with Exception")
				thread1_status = False
				break



##### Thread-2: Node Data Process #####
class data_process(threading.Thread):
	msg_size = 0
	msg_list = []
	key_list1 = []

	def __init__(self, thread_name, msg_queue):
		threading.Thread.__init__(self, name = thread_name)
		self.msg = msg_queue

	## Remove C2M apikey + feedid information from raw data
	def remove_c2m_prefix(self, raw_message):
		prefix1 = ""
		prefix2 = ""
		prefix3 = ""
		if prefix3 in raw_message:
			prefix_length = raw_message.index(prefix3) + len(prefix3)
			data_message = raw_message[prefix_length:]
		else:
			data_message = "Error"

		return data_message


	def split_parameter(self, raw_data, splitter1=',', splitter2='|'):
		processed = {}
		if splitter1 in raw_data and splitter2 in raw_data:
			p1 = raw_data.split(splitter2)
			for item in p1:
				p_index = item.index(splitter1)
				key = item[0:p_index]
				value = item[p_index+1:]
				processed[key] = value
		else:
			processed['Error'] = "unable to find splitters in raw data"

		return processed


	def run(self):
		global thread1_status, thread2_status
		while True:
			
			thread2_status = True
			try:

				if not self.msg.empty():
					self.msg_size = self.msg.qsize()
					for i in xrange (self.msg_size):
						data = self.msg.get()	  ## May need to set up timeout or block in Queue
						self.msg_list.append(data)
						del data

					### Done Fetching From Queue in Current Period ###
					print self.msg_list
					### Data Process Starts From Here ###
	
					del self.msg_list[:]	
					self.msg_size = 0

				elif thread1_status == False:
					break

				else:
				#	ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				#	print("{} Thread 2 {}: Waiting For Message From Queue...").format(ts, self.getName())
					pass

			except Exception as e:
				print("{} Thread-2: {}").format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), self.getName())
				print("-> Exception Error: ", e)
				basic_log("Error", "Thread-2 Terminated with Exception")
				thread2_status = False
				break


#######  System Main Thread (0) #######
def main():
	global msg_queue
	msg_queue = Queue()
	
	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.on_message = on_message 
	mqttc.on_publish = on_publish

	try:
		mqttc.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
	except:
		print("-> Connect to MQTT Broker Failed, Reconnecting...")
		basic_log("Critical", "Connecting to MQTT Broker Failed.")

	mqttc.loop_start()
	mqttc.subscribe(sub_topic)

	thread1 = node_message("node_msg_pub", msg_queue, mqttc)
	thread2 = data_process("node_data_process", msg_queue)


	thread1.start()
	thread2.start()

	thread1.join()
	print("-> End of Thread-1: node_msg_pub @ "+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	thread2.join()
	print("-> End of Thread-2: node_data_process @ "+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))



if __name__ == '__main__':
			##################### Software Information #######################
	print "\n+---------------------------------------------------------------------------+\n"
	print "+                   Welcome to Use Multi-Chat Client App                    +"
	print "\n+----------------------------- Version 1.0.0 -------------------------------+\n"
	print "          >>> Python Back-end Client is Produced by Jason/Ge Wu <<<\n"
			##################################################################
	main()