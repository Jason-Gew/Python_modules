#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# REST API For HTTP - MQTT Publish and Subscribe to certain database.
# Produced By Jason/Ge Wu
# Current Release on Apr/24/2017
from flask import Flask, jsonify, request
import paho.mqtt.subscribe as mqtt_sub
import paho.mqtt.publish as mqtt_pub
import logging
import json
import time
import os

app = Flask(__name__)
#app.config['BASIC_AUTH_USERNAME'] = ''
#app.config['BASIC_AUTH_PASSWORD'] = ''

path_prefix = "/home/jason/python_code/pubsub/"		# Change directory for your system
MQTTv31 = 3
MQTTv311 = 4

mqtt = {
	'broker':{
				'version': '3.1.1',
				'server': '10.0.1.1',
				'port': 1883,
				'login': False
			 },
	'usage':{
				'format': 'application/json',
				'header example': 'Content-Type: application/json',
				'body example': {   "server":"MQTT Broker Address",
									"port":1883,
									"topic":"level1/level2/level3",
									"payload":"This is an example test message.",
									"is_file":False,
									"qos":0,
									"retain":False
						 		},
				'notice': '''Pass Content-Type: application/json in header to declare JSON format data type.
							Pass the parameters in boday as example shows. If payload is a firmware file on server, pass the name of the firmware in payload, and set is_file true.
'''
			}
	}

def list_files(path, suffix=".bin"):
	result = {}
	result['status'] = ""
	result['files'] = []
	try:
		for item in os.listdir(path):
			if item.endswith(suffix):
		#		print(os.path.join(path, item))
				result['files'].append(item)
			else:
				continue
		if len(result['files']) == 0:
			 result['status'] = "No File(s) Found"
		else:
			result['status'] = "Success"

	except OSError as err:
		result['status'] = "Fail: " + str(err[1])
		print err[1]
	finally:
		return result

##### Publish Single Message or File #####
class single_publish:

	broker = "localhost"
	port = 1883
	retain = False
	qos = 0
	keepalive = 15

	def __init__(self, broker, port):
		self.broker = broker
		self.port = port

	def publish_binary_file(self, topic, file_path):
		global path_prefix
		result = {}
		result['status'] = ""
		path = path_prefix+file_path
		print path
		if os.path.exists(path):
			pass
		else:
			print ("\n*** File Does Not Exist ***\n")
			result['message'] = "File does not exist"
			result['status'] = "Fail"
			return result

		if topic == "" or topic.isspace() or topic == '#':
			print("-> Invalid Topic for MQTT File Publish!")
			result['message'] = "Invalid Topic"
			result['status'] = "Fail"
			return result
		else:
			pass

		buf = bytearray(os.path.getsize(path))		# Use byte array to store, instead of string
		with open(path, 'rb') as f:
			f.readinto(buf)

		try:
			mqtt_pub.single(topic, buf, qos=self.qos, hostname=self.broker, port=self.port,
							retain=self.retain, protocol=MQTTv311, keepalive=self.keepalive)

		except Exception as e:
			print("-> Unexpected Error: ",e)
			result['message'] = "MQTT File Publish Fail."
			result['status'] = "Fail"
		else:
			result['message'] = "MQTT File Publish Success."
			result['status'] = "Success"

		finally:
			return result


	def clean_retain(self, topic):
		result = {}
		result['status'] = ""

		if topic == "" or topic.isspace() or topic == '#':
			print("-> Invalid Topic for MQTT Clean Retain!")
			result['message'] = "Invalid Topic."
			result['status'] = "Fail"
			return result
		else:
			pass

		try:
			mqtt_pub.single(topic, None, qos=self.qos, hostname=self.broker, port=self.port,
							retain=self.retain, protocol=MQTTv311)

		except Exception as e:
			print("-> Unexpected Error: ",e)
			result['status'] = "Fail"
			result['message'] = "Failed to Clean Retained Message."

		else:
			result['status'] = "Success"
			result['message'] = "Retained Message Has Been Cleaned."

		finally:
			return result

	def publish_message(self, topic, raw_msg):
		result = {}
		result['status'] = ""

		if topic == "" or topic.isspace() or topic == '#':
			print("-> Invalid Topic for MQTT Message Publish!")
			result['message'] = "Invalid Topic."
			result['status'] = "Fail"
			return result
		else:
			pass

		try:
			mqtt_pub.single(topic, raw_msg, qos=self.qos, hostname=self.broker, port=self.port,
							retain=self.retain, protocol=MQTTv311)

		except Exception as e:
			print("-> Unexpected Error: ",e)
			result['message'] = "MQTT Message Publish Fail."
			result['status'] = "Fail"

		else:
			result['message'] = "MQTT Message Publish Success."
			result['status'] = "Success"
		finally:
			return result


@app.route('/esp8266/firmware', methods = ['GET'])
def get_firmware_list():
	global path_prefix
	result = list_files(path_prefix)

	if 'Fail' not in result['status'] or 'fail' not in result['status']:
		return jsonify(
						status="Success",
						number=len(result['files']),
						firmware=result['files']
					  )
	else:
		return jsonify(
						status="Fail",
						number=len(result['files']),
						firmware=result['files']
					  )


@app.route('/esp8266/mqtt/publish', methods = ['GET', 'POST'])
def mqtt_publish():
	temp = {}
	publish = {}
	forbid_key = ['#', "$SYS", "", "test"]

	if request.method == 'GET':
		return jsonify(mqtt)

	elif request.method == 'POST':
		if request.headers['Content-Type'] == 'text/plain':
			raw = request.data
			if "|" in raw and "=" in raw:
				parameters = raw.split("|")
				try:
					for item in parameters:
						if '=' in item:
							key = item.split("=")[0]
							value = item.split("=")[1]
							temp[key] = value

						else:
							return jsonify(
											status="Unsupported Media Type", 
											code = 415,
											message="Missing parameter or value splitter(s) in plan text data."
										  )

					# process request
					if 'server' in temp.keys():
						if temp['server'] == "" or temp['server'].isspace():
							return jsonify(
											status="Unprocessable Entity", 
											code = 422,
											message="Invalid MQTT server hostname."
										  )
						elif temp['server'] != mqtt['broker']['server']:
							publish['server'] = temp['server']
						else:
							publish['server'] = mqtt['broker']['server']

					elif 'server' not in temp.keys():
						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Missing MQTT server address."
									  )

					if 'port' in temp.keys():
						if temp['port'] == "" or temp['port'].isspace():
							return jsonify(
											status="Unprocessable Entity", 
											code = 422,
											message="Invalid MQTT server port."
										  )
						elif int(temp['port']) != mqtt['broker']['port']:
							publish['port'] = int(temp['port'])
						else:
							publish['port'] = mqtt['broker']['port']

					elif 'port' not in temp.keys():
						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Missing MQTT server port."
									  )

					if 'topic' in temp.keys():
						if temp['topic'] in forbid_key:
							return jsonify(
											status="Unprocessable Entity", 
											code = 422,
											message="Invalid MQTT topic."
										  )
						else:
							publish['topic'] = temp['topic']

					elif 'topic' not in temp.keys():
						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Missing MQTT topic."
									  )

					if 'payload' not in temp.keys():
						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Missing MQTT message payload."
									  )

					if 'is_file' not in temp.keys():
						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Missing MQTT message or file indicator (is_file)."
									  )
					elif temp['is_file'] == "true" or temp['is_file'] == "True" or temp['is_file'] == "1":
						publish['is_file'] = True
					else:
						publish['is_file'] = False

					if 'qos' in temp.keys():
						publish['qos'] = int(temp['qos'])
					else:
						publish['qos'] = 0

					if 'retain' in temp.keys():
						if temp['retain'] == "True" or temp['retain'] == "true" or temp['retain'] == '1':
							publish['retain'] = True
						else:
							publish['retain'] = False
					else:
						publish['retain'] = False

				#	return jsonify(publish)
				#	print(publish)
					if publish['is_file']:
						mqttc = single_publish(publish['server'], int(publish['port']))
						mqttc.qos = int(publish['qos'])
						mqttc.retain = publish['retain']
						result = mqttc.publish_binary_file(publish['topic'], temp['payload'])
						return jsonify(result)

					else:

						return jsonify(
										status="Unprocessable Entity", 
										code = 422,
										message="Plain text body is only for publishing valid firmware file."
									  )


				except Exception as err:
					return jsonify(
									status="Internal Server Error", 
									code = 500,
									message="Server Error: " + str(err)
								  )

			else:
				print("-> Unable to find splitters in plain text data")
				return jsonify(
								status="Unsupported Media Type", 
								code = 415,
								message="Unable to find parameter or value splitter(s) in plain text data."
							  )

		## Process JSON format Request
		elif request.headers['Content-Type'] == 'application/json':

			temp = request.json
			if 'server' in temp.keys():
				if temp['server'] == "" or temp['server'].isspace():
					return jsonify(
									status="Unprocessable Entity", 
									code = 422,
									message="Invalid MQTT server hostname."
								  )
				elif temp['server'] != mqtt['broker']['server']:
					publish['server'] = temp['server']
				else:
					publish['server'] = mqtt['broker']['server']

			elif 'server' not in temp.keys():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Missing MQTT server address."
							  )

			if 'port' in temp.keys():
				if temp['port'] == "" or temp['port'] == None:
					return jsonify(
									status="Unprocessable Entity", 
									code = 422,
									message="Invalid MQTT server port."
								  )
				elif int(temp['port']) != mqtt['broker']['port']:
					publish['port'] = int(temp['port'])
				else:
					publish['port'] = mqtt['broker']['port']

			elif 'port' not in temp.keys():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Missing MQTT server port."
							  )

			if 'topic' in temp.keys():
				if temp['topic'] in forbid_key:
					return jsonify(
									status="Unprocessable Entity", 
									code = 422,
									message="Invalid MQTT topic."
								  )
				else:
					publish['topic'] = temp['topic']

			elif 'topic' not in temp.keys():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Missing MQTT topic."
							  )

			if 'payload' not in temp.keys():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Missing MQTT message payload."
							  )

			if 'is_file' not in temp.keys():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Missing MQTT message or file indicator (is_file)."
							  )
			elif temp['is_file'] == "true" or temp['is_file'] == "True" or temp['is_file'] == "1" or temp['is_file'] == True:
				publish['is_file'] = True
			else:
				publish['is_file'] = False

			if 'qos' in temp.keys():
				publish['qos'] = int(temp['qos'])
				if publish['qos'] > 3 or publish['qos'] < 0:
					return jsonify(
									status="Unprocessable Entity", 
									code = 422,
									message="Invalid MQTT QoS."
								  )
			else:
				publish['qos'] = 0

			if 'retain' in temp.keys():
				if temp['retain'] == "True" or temp['retain'] == "true" or temp['retain'] == '1' or temp['retain'] == True:
					publish['retain'] = True
				else:
					publish['retain'] = False
			else:
				publish['retain'] = False

		#	return jsonify(publish)
			print(publish)
			if publish['is_file']:
				mqttc = single_publish(publish['server'], int(publish['port']))
				mqttc.qos = publish['qos']
				mqttc.retain = publish['retain']
				result = mqttc.publish_binary_file(publish['topic'], temp['payload'])
				return jsonify(result)

			else:
				mqttc = single_publish(publish['server'], int(publish['port']))
				mqttc.qos = int(publish['qos'])
				mqttc.retain = publish['retain']
				result = mqttc.publish_message(publish['topic'], temp['payload'])
				return jsonify(result)

	#		return jsonify(temp)


		elif 'parameter' in request.headers:
			return 'Header Data: ' + request.headers['data']

		else:
			return jsonify(
							status = "Unsupported Media Type", 
							code = 415,
							message = "Please use JSON format in request body.")

# Clean Retained Message
@app.route('/esp8266/mqtt/clean_retain', methods = ['POST'])
def mqtt_clean_retain():
	temp = {}
	publish = {}
	forbid_key = ['#', "$SYS", "", "test"]

	if request.headers['Content-Type'] == 'text/plain':
		return jsonify(
						status = "Unprocessable Entity", 
						code = 422,
						message = "Please use JSON format in request body."
					  )

	## Process JSON format request
	elif request.headers['Content-Type'] == 'application/json':
		temp = request.json
		if 'server' in temp.keys():
			if temp['server'] == "" or temp['server'].isspace():
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Invalid MQTT server hostname."
							  )
			elif temp['server'] != mqtt['broker']['server']:
				publish['server'] = temp['server']
			else:
				publish['server'] = mqtt['broker']['server']

		elif 'server' not in temp.keys():
			return jsonify(
							status="Unprocessable Entity", 
							code = 422,
							message="Missing MQTT server address."
						  )

		if 'port' in temp.keys():
			if temp['port'] == "" or temp['port'] == None:
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Invalid MQTT server port."
							  )
			elif int(temp['port']) != mqtt['broker']['port']:
				publish['port'] = int(temp['port'])
			else:
				publish['port'] = mqtt['broker']['port']

		elif 'port' not in temp.keys():
			return jsonify(
							status="Unprocessable Entity", 
							code = 422,
							message="Missing MQTT server port."
						  )

		if 'topic' in temp.keys():
			if temp['topic'] in forbid_key:
				return jsonify(
								status="Unprocessable Entity", 
								code = 422,
								message="Invalid MQTT topic."
							  )
			else:
				publish['topic'] = temp['topic']

		elif 'topic' not in temp.keys():
			return jsonify(
							status="Unprocessable Entity", 
							code = 422,
							message="Missing MQTT topic."
						  )
		else:
			pass

		mqtt_clean = single_publish(publish['server'], int(publish['port']))
		mqtt_clean.retain = True
		result = mqtt_clean.clean_retain(publish['topic'])
		return jsonify(result)


	else:
		return jsonify(
						status = "Unsupported Media Type", 
						code = 415,
						message = "Unidentified Header Content-Type."
					  )


if __name__ == '__main__':
	app.run(debug=True, host="localhost", port = 80)