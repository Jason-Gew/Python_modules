#!/usr/bin/env python
# Simple encryption/decryption Module
# For less-strong data encryption/decryption, fast process.
# The module will be kept updating...
#
# Produced By Jason/Ge Wu
#

from Crypto.Cipher import AES
from Crypto.Cipher import XOR
import base64
import time
import os

def encrypt_xor(key, message):
	status = False
	encrypted = ""
	if len(key) < 6 or key.isspace():
		return status, encrypted
	elif key.isdigit():
		return status, encrypted
	else:
		cipher = XOR.new(key)
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		encrypted = base64.b64encode(timestamp+cipher.encrypt(message))
		status = True
		return status, encrypted

def decrypt_xor(key, ciphertext):
	cipher = XOR.new(key)
	decode = base64.b64decode(ciphertext)
	origin_timestamp = decode[0:19]
	msg = cipher.decrypt(decode[19:])
	return origin_timestamp, msg


if __name__ == '__main__':
	message = raw_input("Please Input Your Message: ")
	key = raw_input("Please Input Your Key: ")

	status, encoded = encrypt_xor(key, message)
	if status:
		print encoded
		ts, origin = decrypt_xor(key, encoded)
		print ts, ':', origin
	else:
		print "invalid key"