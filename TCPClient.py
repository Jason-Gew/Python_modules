#!/usr/bin/env python
# Basic single thread TCP Client...

import socket
import sys
import time


HOST = raw_input("Please enter the TCP Server Address: ")
PORT = int(raw_input("Please enter the TCP Server Port: "))

while True:
	message = raw_input("-> ")
	# data = message.join(sys.argv[1:])
	data = message
	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connect to server and send data
		sock.connect((HOST, PORT))
		sock.sendall(data + "\n")

		# Receive data from the server and shut down
		received = sock.recv(1024)
	finally:
		sock.close()
	print "+-------------------{}---------------------+".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
	print "Sent: {}".format(data)
	print "Received: {}".format(received)
