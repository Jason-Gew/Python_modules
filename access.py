#!/usr/bin/env python
# 1.Monitor last (ssh/login) access of the current Linux system.
# 2.Track specific user ssh/login the system.
# 3.Send access report to remote server.
#
# Created By Jason/Ge Wu

import requests
import json
import time
import os


log_path = "file/access_log.json"

def read_last_cmd(name=[], time_range=""):
	result = {}
	if len(name)>0:
		for i in xrange(len(name)):
			if name[i].isspace() or name[i]=="":
				print("Invalid Name Found in {} Place of the List").format(i)
				continue
			else:				
				cmd = "last | grep "+name[i]
				raw_records = os.popen(cmd, 'r').readlines()
				result[name[i]] = raw_records
	else:
		raw_records = os.popen("last", 'r').readlines()
		result['record'] = raw_records

	return result


def read_lastlog_cmd(name=[]):
	result = {}
	if len(name)>0:
		for i in xrange(len(name)):
			if name[i].isspace() or name[i]=="":
				print("Invalid Name Found in {} Place of the List").format(i)
				continue
			else:
				cmd = "lastlog | grep "+name[i]
				raw_records = os.popen(cmd, 'r').readlines()
				length = len(raw_records)
				if length > 0:
					result[name[i]] = raw_records[0][26:-1]
		#			print raw_records
		#			print raw_records[0][26:-1]
				else:
					result[name[i]] = str(raw_records)
	else:
		print("-> Must Provide Valid User Name!")

	return result


def result_process(result={}):
	value = []
	processed = {}
	no_record = "**Never logged in**"
	for key in result.keys():
		value = result[key]
		if value == "":
			print("-> Cannot find record for user [{}]").format(key)
			processed[key] = ""
		elif no_record in value:
			print("-> User [{}] has not logged in yet!").format(key)
			processed[key] = ""
		else:
			processed[key] = value

	return processed


def read_history(path):
	result = {}
	try:
		with open(path) as history:
			records = json.load(history)
			if "history" in records.keys():
				result = records["history"]
				if len(result) == 0:
					print("-> No historical data.")
				else:
					pass
			else:
				print("-> No Keywords Found.")

		if "timestamp" in records.keys():
				print("-> Last Updating Timestamp: {}").format(records["timestamp"])

	except IOError:
		print "-> Please check the Configuration File Path!\n"
		exit(1)

	except KeyError:
		print "-> Invalid Key Word(s) in JSON File!\n"
		exit(1)

	except ValueError:
		print "-> Invalid content or syntax in the config file!\n"
		exit(1)
	else:
		return result


def update_history(path, content):
	result = {"history":{}}
	status = False

	if len(content) == 0:
		print("-> No Records")
		return False
	else:
		result["history"] = content
		current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		result["timestamp"] = current_time

	try:
		with open(path, 'w') as update:
			json.dump(result, update, indent=4, sort_keys=False)

	except IOError:
		print "-> Please check the Configuration File Path!\n"
		status = False

	except KeyError:
		print "-> Invalid Key Word(s) in JSON File!\n"
		status = False

	except ValueError:
		print "-> Invalid content or syntax in the config file!\n"
		status = False
		
	except:
		print "\n*** Unexpected Error ***\n*** Please Contact the Administrator ***\n"
		status = False
	else:
		status = True

	return status

### Https POST to C2M ###
def c2m_https_post(user, info):
	global event_apikey, event_feedid 
	timeout = 5
	status = 0
	c2m_api = "https://ice.c2m.net/Ice.svc/PostFeed?apikey="
	destination = c2m_api + apikey + '&feedID=' + feedid

	event_msg = "user,"+user+"|info,"+info
	header_parameter = {}
	header_parameter['feed'] = event_msg

	try:
		resp = requests.post(url=destination, headers=header_parameter, timeout=timeout)
		status = resp.status_code
		if status == 200:
			print("-> HTTPS POST Success")
		else:
			print("-> HTPPS POST Fail: ", status)

	except requests.exceptions.RequestException as e:
		print("-> HTTPS POST Error: {}").format(e)

	finally:
		del event_msg

##  Update beacon event via TCP  ##
def update_event(user, info):
	global apikey, feedid
	result = False
	event = c2m_tcp(apikey, feedid)

	event_msg = "user,"+user+"|info,"+info
	
	try:
		event_result = event.send(event_msg)
	except Exception as err:
		print ("-> TCP Unexpected Error. Please Check Network Connection & C2M Server...")
		
	else:
		if event_result['send'] == True:
			print ("-> Update Event Success")
			result = event_result['send']
		else:
			print ("-> Update Event Fail 1st time: ",event_result['error']) 
	finally:
		del event_msg
		return result

def main():
	try:	
		user = ["root","pi"]
		result = {}
		history = {}
		update_records = {}
		update_flag = False

		history = read_history(log_path)
		print "-> Historical Records: ",history

		result = read_lastlog_cmd(user)
		processed = result_process(result)
		print "-> ",processed


		for key in processed.keys():
			if key in history.keys():
				if processed[key] == history[key]:
					print("-> No Update Status for User [{}]").format(key)
				else:
					print("-> Update Status for User [{}]").format(key)
					update_flag = True
					update_records[key] = processed[key]
					report = update_event(key, processed[key])
			elif key not in history.keys():
				print("-> New Status Found on User [{}]").format(key)
				update_records[key] = processed[key]
			else:
				pass

		for key in history.keys():
			if key not in processed.keys():
				update_records[key] = history[key] 
			else:
				continue

		if update_flag:
			status = update_history(log_path, processed)
			print status

	except Exception as err:
		print("-> Unexpected Error:")
		print err

if __name__ == "__main__":
	while True:
		main()
		time.sleep(5)