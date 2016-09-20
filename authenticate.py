#!/usr/bin/env python
#
# authenticate.py module is create by Jason/Ge Wu
# Purpose to fast set up and verify username & password
# for system or software access.

from getpass import getpass	# Disable password display on console
import base64				# If necessary, use more advanced encryption such as AES, MD5

encryp_pass = ""


def set_authentication(pass_length, set_timeout):
	global encryp_pass
	while set_timeout > 0:
		select1 = raw_input("\nWould you like to setup a new Password for Login? (Y/n): ")
		if select1 == 'Y' or select1 == 'y':
			while set_timeout > 0:
				buff1 = getpass(prompt = "\nPlease Enter your Password: ")
				if not buff1.isspace():
					buff2 = getpass(prompt = "Please Enter your Password again: ")
					if buff1 == buff2:
						if len(buff2) < pass_length:
							print "-> Password must have {} characters or more!".format(pass_length)
							set_timeout -= 1
							print "-> You have {} chance(s)...".format(set_timeout)
							continue
						else:
							encryp_pass = base64.b64encode(buff2)
							print "\n ==== Password Setup Success ====\n"
							del buff1, buff2
							return True
					else:
						print "-> Password does not match! Please Try Again!\n"
						set_timeout -= 1
						print "-> You have {} chance(s)...".format(set_timeout)
						continue
				else:
					print "-> Invalid Password!\n"
					set_timeout -= 1
					print "-> You have {} chance(s)...".format(set_timeout)
					continue

		elif select1 == 'N' or select1 == 'n':
			return False
			break			
		else:
			if set_timeout > 0:
				print "-> Please enter \'Y\' or \'n\' character only!"
				set_timeout -= 1
				print "-> You have {} chance(s)...".format(set_timeout)
			else:
				print "\nTime Out, please re-run the program and Try Carefully!\n"
				exit(1)
		

def console_authenticate(set_timeout):
	while set_timeout > 0:
		buff = getpass(prompt = "\nPlease enter your Password: ")
		encryp_buffer = base64.b64encode(buff)
		if encryp_buffer == encryp_pass:
			print "\n ==== Authentication Success ==== \n"
			del buff, encryp_buffer
			return True
		elif buff == '':
			print "-> Password cannot be empty!\n"
			set_timeout -= 1
			print "-> You have {} chance(s)...".format(set_timeout)
		else:
			set_timeout -= 1
			if set_timeout > 0:
				print "-> Invalid Password, Please Try Again!"
				print "-> You still have {} chance(s)...".format(set_timeout)
			else:
				print "\n ==== Authentication Fail ==== \n"
				return False

# For testing purpose...
if __name__ == "__main__":
	if set_authentication(6,4):

		if console_authenticate(3):
			print "Done"
		else:
			print "Failed"
			exit(1)
	else:
		print "No Authentication!"
		exit(0)
