#!/usr/bin/env python
'''
 <https_post.py> is produced by Jason/Ge Wu in order to transmit data to C2M Cloud
	c2m_https utilizes POST method with JSON / XML data format.
	pass the original_data as Python-Dictionary type.

	Current Release on Jun/24/2016 
'''

from collections import OrderedDict
import requests
import time
import base64
import json

api_url = ""

class https_post:
	''
	def __init__(self, apikey, feedid):
		self.apikey = apikey
		self.feedid = feedid

	def __del__(self):
		class_name = self.__class__.__name__

	def format2json(self,original_data):
		json_data = json.dumps(original_data,sort_keys=False)
		return json_data

	def format2xml(self,original_data):
		print "This Method is not available now, please use <format2json>.\n"
		exit(1)

	def post(self,data):

		if self.apikey and self.apikey.isspace():
			print "Invalid Apikey!\n"
			exit(1)
		elif self.feedid and self.feedid.isspace():
			print "Invalid FeedID!\n"
			exit(1)
		else:
			destination = api_url + self.apikey + '&feedID=' + self.feedid

		final_message = base64.b64encode(data)
		print "Length of the Message: %d Bytes" % len(final_message)
		h = {}
		h['feed'] = final_message
		try:
			resp = requests.post(url=destination, headers=h)
			status = resp.status_code
			print "Message POST Success @",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			del final_message
			return status
		except:
			print "Message POST Fail @",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			del final_message
			return "Please check the network!"

## Make comment of the "main" below when you are using this module
if __name__ == "__main__":
	apikey = ""
	feedid = ""
	current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	test1 = [{
				"uuid":"1234sdfklsjgsdfg",
				"edge_id":99,
				"event_id":"entry",
				"event_time":current_time,
				"duration":0
			}
			]
	test2 = [
			[
			{"duration":0},
			{"event_time":current_time},
			{"event_id":"entry"},
			{"edge_id":1245},
			{"uuid":"1234sdfklsjgsdfg"}
			]
			]

	print test1
	print " =============== "
	s = https_post(apikey,feedid)
	final = s.format2json(test1)
	print final
	check = s.post(final)
	print check