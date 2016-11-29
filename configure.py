#!/usr/bin/env python
# configure.py is for reading basic plain text, json, xml configuration file.
# Configuration files must follow the basic format structure:
# 
# Module is produced by Jason/Ge Wu
# Current Release on Nov/20/2016

import xml.etree.ElementTree as XML_ET
import ConfigParser
import json
import time
import os

class read_config:

	size = 0
	path = ""
	status = ""
	
	def __init__(self, file_path):
		self.path = file_path

	def __check_exist(self, file_path):
		if os.path.exists(file_path):
			return True
		else:
			print ("\n*** File Does Not Exist ***\n")
			return False

	# This method reads JSON config file and returns original JSON data in Python Dictionary.
	def read_raw_json(self):
		info = {}

		if self.__check_exist(self.path):
			pass
		else:
			info['error'] = "invalid path"
			return info

		try:
			with open(self.path,'r') as origin:
				info = json.load(origin)
		except IOError:
			print "-> Please Check the Configuration File Path!\n"
			info['error'] = "invalid path"
			return info
		except ValueError:
			print "-> Invalid content or syntax in the config file!\n"
			info['error'] = "invalid content"
			return info
		except KeyError:
			print "-> Invalid Key Word(s) in JSON File!\n"
			info['error'] = "invalid json"
			return info		
		except:
			print "-> Unidentified Error! \n"
			infor['error'] = "unidentified error"
		else:
			origin.close
			return info

	# Passing keywords as Python List, the method returns results as Python Dictionary
	# - Debugging -
	def read_json(self, keywords):
		results = {}
		temp = {}
		self.size = len(keywords)
		if (len(keywords)) == 0:
			results['error'] = "empty keywords"
			return results
		else:
			for i in range(len(keywords)):
				if keywords[i] == '':
					results['error'] = "invalid keywords"
					return results
				elif type(keywords[i]) != type(self.path):
					print type(keywords[i])
					results['error'] = "invalid type"
					return results
				else:
					pass

		if self.__check_exist(self.path):
			pass
		else:
			results['error'] = "invalid path"
			return results

		try:
			with open(self.path,'r') as origin:
				temp = json.load(origin)

			for i in range(len(keywords)):
				if keywords[i] in temp:
					print keywords[i]
					if type(temp[keywords[i]]) == type(temp):
						print "check 2"
						for n in range(len(keywords)):
							if keywords[n] in temp[keywords[i]]:
								print "check 3:", n
								if type(temp[keywords[i]][keywords[n]]) == type(temp):
									for m in range(len(keywords)):
										print "check 4: ",m
										if keywords[m] in temp[keywords[i]][keywords[n]]:
											key_name = keywords[i]+'_'+keywords[n]+'_'+keywords[m]
											results[key_name]= temp[keywords[i]][keywords[n]][keywords[m]]
										else:
											print "check 5"
											pass
										#	key_name = keywords[i]+'_'+keywords[n]
										#	results[key_name] = temp[keywords[i]][keywords[n]]
								else:
									key_name = keywords[i]+'_'+keywords[n]
									results[key_name] = temp[keywords[i]][keywords[n]]
							else:
								self.status = keywords[i]+" require sub arguments"
								results['error'] = self.status
					else:
						print "check 7"
						key_name = keywords[i]
						results[key_name] = temp[keywords[i]]
				else:
					print "check 8"
					pass
				#	results['error'] = "no matches"

		except IOError:
			print "-> Please Check the Configuration File Path!\n"
			results['error'] = "invalid path"
			return results

		except KeyError:
			print "-> Invalid Key Word(s) in JSON File!\n"
			results['error'] = "invalid json"
			return results

		except ValueError:
			print "-> Invalid content or syntax in the config file!\n"
			results['error'] = "invalid content"
			return results

		except:
			print "-> Unidentified Error! \n"
			results['error'] = "unidentified error"

		else:
			origin.close
			print "Find Keys: ",results.keys()
			return results


	# Read Plain Text config file: each line should only contain one type of information.
	# Use '=' to distinguish key name with content, ',,' to split multiple elements in a content.
	# If using any speical identifer, please define and pass it to the method.
	# This mehtod returns information as Python Dictionary.
	def read_raw_text(self, identifer='=', splitter=',,'):
		info = {}
		temp = []
		section = ""
		if self.__check_exist(self.path):
			pass
		else:
			info['error'] = "invalid path"
			return info
		try:
			with open(self.path,'r') as origin:
				for lines in origin.readlines():
					settings = lines.strip('\n')
					temp.append(settings)
			self.size = len(temp)

			for l in range (len(temp)):
				if '[' in temp[l]:
					if ']' in temp[l]:
						section = temp[l][(temp[l].find('[')+1):(temp[l].find(']'))]
					else:
						info['error'] = "invalid section"
				elif temp[l].isspace() or len(temp[l])==0:
					continue

				elif identifer in temp[l]:
					key_index = temp[l].index(identifer)
					if len(section) != 0:
						key_name = section + '_' + temp[l][0:key_index]
					else:
						key_name = temp[l][0:key_index]

					if splitter in temp[l][key_index+1:]:
						element = temp[l][key_index+1:].split(splitter)
						info[key_name] = element
					else:
						info[key_name] = temp[l][key_index+1:]
				else:
					if'[' not in temp[l] and ']' not in temp[l]:
						info['error'] = "no identifer in line: "+str(l+1)
					else:
						pass

		except IOError:
			print "-> Please Check the Configuration File Path!\n"
			info['error'] = "invalid path"
			return info
		except:
			print "-> Unidentified Error! \n"
			info['error'] = "unidentified error"
			return info
		else:
			origin.close()
			return info

	# Read XML Configuration File: Must validate the xml first, 
	# make sure to keep list of data in one sperate element.
	# This mehtod returns information as Python Dictionary.
	def read_raw_xml(self):
		info = {}
		if self.__check_exist(self.path):
			pass
		else:
			info['error'] = "invalid path"
			return info

		try:
			tree = XML_ET.parse(self.path)
			root = tree.getroot()
		#	print ("-> XML Root has {} Primary Keys...").format(len(root))
			self.size = len(root)
			if self.size == 0:
				info['error'] = "empty keywords"
				return info
			else:
				pass

			for i in range (len(root)):
			#	print "No.{} Primary Key: {}".format(i, root[i].tag)
				if (root[i].text).isspace():
					sub_size = len(root[i])
					for t in range (sub_size):
						temp = []
					#	print ("Sub Key: {} , Value: {}").format(root[i][t].tag, root[i][t].text)
						if t == 0 and (t+1) == sub_size:
							key_name = root[i].tag + '_' + root[i][t].tag
							info[key_name] = root[i][t].text
						elif t == 0 and root[i][t].tag != root[i][t+1].tag and (t+1) != sub_size:
							key_name = root[i].tag + '_' + root[i][t].tag
							info[key_name] = root[i][t].text            
						elif t == 0 and root[i][t].tag == root[i][t+1].tag and (t+1) != sub_size:
							key_name = root[i].tag + '_' + root[i][t].tag
							temp.append(root[i][t].text)
							info[key_name]=temp
						elif t != 0 and root[i][t].tag != root[i][t-1].tag:
							key_name = root[i].tag + '_' + root[i][t].tag
							info[key_name] = root[i][t].text
						elif t != 0 and root[i][t].tag == root[i][t-1].tag:
							key_name = root[i].tag + '_' + root[i][t].tag
							info[key_name].append((root[i][t].text))
						else:
							pass
						del temp
			#	elif (root[i].text).isinstance():
			#		info['error'] = "invaid structure"
			 	else:
					key_name = root[i].tag
					info[key_name] = root[i].text

		except AttributeError:
			info['error'] = "invaid attribute"

		except:
			info['error'] = "unexpected error"

		else:
			return info


class update_config:

	path = ""
	size = 0
	status = {}

	def __init__(self, file_path):
		self.path = file_path

	def __check_exist(self, file_path):
		if os.path.exists(file_path):
			return True
		else:
			print ("\n*** File Does Not Exist ***\n")
			return False

	# Pass the keywords and content as Python Dictionary, 
	# Keywords hierarchy must be exact same as defined in config file.
	# This method only allow update information, does not offer adding keyword(s).
	def update_json(self, keywords):
		info = {}

		if self.__check_exist(self.path):
			pass
		else:
			info['error'] = "invalid path"
			return info

		self.size = len(keywords)
		if self.size == 0:
			info['error'] = "empty keywords"
			return info
		elif type(keywords) != type(info):
			info['error'] = "invalid keywords type"
			return info
		else:
			pass

		try:
			with open(self.path) as origin:
				info1 = json.load(origin)
			origin.close()

			info1_keys = set(info1.keys())
			keywords_keys = set(keywords.keys())
			if len(keywords_keys - info1_keys) != 0:
				info['error'] = "additional keywords exist"
				return info
			else:
				pass



		except IOError:
			print "-> Please Check the Configuration File Path!\n"
			info['error'] = "invalid path"
			return info
		except ValueError:
			print "-> Invalid content or syntax in the config file!\n"
			info['error'] = "invalid content"
			return info
		except KeyError:
			print "-> Invalid Key Word(s) in JSON File!\n"
			info['error'] = "invalid json"
			return info		
		except:
			print "-> Unidentified Error! \n"
			infor['error'] = "unidentified error"
		else:
			origin.close
			return info



## Comment below lines if use as independent module
if __name__ == '__main__':
	config_file = "file/sample_config.json"
	retrieve = {}

	t = read_config(config_file)
	retrieve= t.read_raw_json()
	print retrieve

