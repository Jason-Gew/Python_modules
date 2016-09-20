#!/usr/bin/env python
# basic argument parser example, for passing different types of arguments into the program
# 

import argparse
import time
import sys


def show_time(mode):
	print "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	if mode == '1':
		print "Current Datetime: ", time.asctime()
	elif mode == '2':
		print "UNIX Timestamp: ", int(time.time())
	elif mode == '3':
		print "Datetime: ", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

	else:
		print "[{}] is an invalid mode!\n".format(mode)

	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

def main():
	parser = argparse.ArgumentParser(usage='%(prog)s [-options]')

	parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s 1.0.0')
	parser.add_argument('-e', '--enable', action = 'store_true', dest = 'enable', default = False,
						help = 'enable function_')
	parser.add_argument('-d', '--disable', action = 'store_true', dest = 'disable', default = False,
						help = 'disable function_')
	parser.add_argument('-t', '--time', type = show_time, help = 'show system time with multiple format')

	parser.add_argument('-u', '--user',  dest = 'username', default = '', help = 'enter username to the system')
	parser.add_argument('-p', '--parameter', nargs = '?', dest = 'parameter', default = [], 
						help = 'pass parameters to the system' )

	parser.add_argument('-s','--select', dest = 'select', default = '', choices = ['option1', 'option2', 'option3'],
						help = 'select system defined options')

	results = parser.parse_args()

	print "\n[ {} ] Argument(s) Passed...".format(len(sys.argv)-1)

	print "Enable : ", results.enable
	print "Disable : ", results.disable
	print "User: ", results.username
	print "Parameter: ", results.parameter
	print "Select: ", results.select


if __name__ == "__main__":
	main()