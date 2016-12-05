#!/usr/bin/env python
# cpu_temp.py is to read the CPU/GPU chip temperature on Raspberry Pi
# If implementing on other Linux machine, please use the path below
# "cat /sys/class/thermal/thermal_zone0/temp"
# Module is produced by Jason/Ge Wu
import os

def cpu_temperature(unit = 'c'):
	temp = os.popen('vcgencmd measure_temp').readline()
	temp_num = float(temp.replace('temp=',"").replace("'C\n",""))
#	temp0 = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
#	temp0_num = float(temp0.replace('\n',''))/1000
#	print ("CPU Temperature: {}\nGPU Temperature: {}").format(temp0_num, temp_num)
	if unit == 'c':
		return temp_num
	elif unit == 'f':
		return (temp_num * 1.8 + 32)
	else:
		print "Invalid Temperature Unit"
		return -99
	
# Make comment of below lines if use as a module
if __name__ == '__main__':
	temp_c = cpu_temperature()
	print temp_c
