#!/usr/bin/env python
# Simple encryption/decryption Module
# For less-strong stream message encryption/decryption, fast process.
# The module will be kept updating...
#
# Produced By Jason/Ge Wu
#

from Crypto.Cipher import AES
from Crypto.Cipher import XOR
import base64
import time
import os


class XOR_encrypt:
	__key_length = 6

	def __init__(self, key):
		self.__key = key

	# Check if key has more than defined length characters,
	# Avoid of all space, all digits and all low cases.
	def __check_key(self):
		if len(self.__key) < self.__key_length or self.__key.isspace():
			print "Encryption key shoud have at least {} characters.".format(self.__key_length)
			return False
		elif self.__key.isdigit():
			print "Encryption key cannot be all digits."
			return False
		elif self.__key.islower():
			print "Encryption key should contain at least 1 capital character."
		else:
			return True

	# This method will encrypt the original message by XOR,
	# after adding an UNIX timestamp then encrypt again by base64.
	# Method returns status value and cipher_message
	def encrypt_xor(self, message):
		status = False
		encrypted = ""
		
		if self.__check_key():
			cipher = XOR.new(self.__key)
		#	timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			timestamp = str(int(time.time()))
			encrypted = base64.b64encode(cipher.encrypt(message)+timestamp)
			status = True
			return status, encrypted
		else:
			status = False
			return status, encrypted

	# This method will decrypt the cipher message first by base64,
	# after cutting an UNIX timestamp then decrypt again by XOR.
	# Method returns orginial timestamp and message
	def decrypt_xor(self, ciphertext):
		cipher = XOR.new(self.__key)
		try:
			decode = base64.b64decode(ciphertext)
			ts = decode[-10:]
		except TypeError:
			print "Incorrect Padding"
			origin_timestamp = "invalid"
			msg = "invalid"
			return origin_timestamp, msg
		else:
			try:
				origin_timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(ts)))
			except ValueError:
				print "Incorrect Timestamp"
				origin_timestamp = "invalid"

			msg = cipher.decrypt(decode[0:-10])
			return origin_timestamp, msg


class AES_encrypt:
	__block_size = 16
	
	
if __name__ == '__main__':
	message = raw_input("Please Input Your Message: ")
	key = raw_input("Please Input Your Key: ")

	e = XOR_encrypt(key)
	status, encoded = e.encrypt_xor(message)
	if status:
		print encoded
		ts, origin = e.decrypt_xor(encoded)
		print ts, ':', origin
	else:
		print "invalid key"