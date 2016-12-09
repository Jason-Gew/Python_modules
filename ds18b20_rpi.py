#!/usr/bin/env python
# DS18B20 Temperature Sensor on Raspberry Pi
# One-Wire GPIO should be enabled in /boot/config.txt | dtoverlay=w1-gpio
# Require the MAC address of the connected DS18B20(s)
#
# Resource from website, modified by Jason/Ge Wu

from glob import glob
import time
import os

def read_temp_raw(path):
	f = open(path, 'r')
	lines = f.readlines()
	f.close()
	return lines

def temp_process(raw_data, unit='c'):
	lines = raw_data
	while lines[0].strip()[-3:] != 'YES':
		print "-> CRC Verification Failed, Will Check in the Next Period!"
		time.sleep(0.5)
		lines = read_temp_raw()

	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		if unit == 'c' or unit == 'C':
			temp_c = float(temp_string) / 1000.0
			return temp_c
		elif unit == 'f' or unit == 'F':
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			return temp_f
		else:
			return (0.00)
	else:
		pass

if __name__ == '__main__':
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	base_dir = '/sys/bus/w1/devices/'
	try:
		device_folder = glob(base_dir + '28*')[0]
		device_file = device_folder + '/w1_slave'
		sensor_addr = device_folder.replace(base_dir,'')
	except IndexError:
		print "\n-> No Valid DS18B20 Found\n-> Please check the sensor connection and config setup!\n"
		exit(1)
	except:
		print "-> Unexpected Error!\n"
		exit(1)
	else:
		print "-> Find DS18B20 Address: ", sensor_addr
		while True:
			raw = read_temp_raw(device_file)
			print ('[ {} ]').format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
			print "-> Current Temperature: " + str(temp_process(raw))+ ' \'C' + "\n"
			time.sleep(10)




