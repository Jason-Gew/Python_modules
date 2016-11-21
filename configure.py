#!/usr/bin/env python
# configure.py is for reading basic plain text, json, xml configuration file.
# Configuration files must follow the basic format:
# 
# Module is produced by Jason/Ge Wu
# Current Release on Nov/20/2016

import json
import time
import xml
import os

class read_config:

	file_size = 0
	path = ""
	buff = ""
	status = {}
	
	def __init__(self, file_path):
		self.path = file_path

	def __check_exist(self, file_path):
		if os.path.exists(file_path):
			return True
		else:
			print ("\n*** Log File Does Not Exist ***\n")
			return False

	def read_json_origin(self):
		info = {}

		if self.__check_exist(self.path):
			pass
		else:
			info['error'] = "invalid path"

		try:
			with open(self.path) as origin:
				info = json.load(origin)
		except IOError:
			print "-> Please Check the Configuration File Path!\n"
			info['error'] = "invalid path"
			return info
		except ValueError:
			print "-> Invalid content or syntax in the config file!\n"
			info['error'] = "invalid content"
			return info
		except:
			print "-> Unidentified Error! \n"
			infor['error'] = "unidentified error"
		else:
			origin.close
			return info

	def read_text_origin(self):


	def read_json(self, keywords):

## Comment below lines if use as independent module
if __name__ == '__main__':
	config = "sample_config.json"
	retrieve = {}
	t = read_config(config)
	retrieve= t.read_json_origin()
	print retrieve

