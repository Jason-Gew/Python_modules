#!/usr/bin/env python
# Basic single thread TCP Server

import SocketServer
import socket
import time



response = "Received"


class MyTCPHandler(SocketServer.BaseRequestHandler):
	"""
	The RequestHandler class for server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""
	def handle(self):
		# self.request is the TCP socket connected to the client,buffer size: 1024
		self.data = self.request.recv(1024).strip()
		print "-------------------------------------------------------"
		print "{} Send:".format(self.client_address[0])
		print self.data
		print "[ Received Time:", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"]"+" [Length:"+str(len(self.data))+']'
		print "-------------------------------------------------------"
		# Send back the response
		self.request.sendall(response)

def address_check(ip_address):
	try:
		result = socket.gethostbyaddr(ip_address)
		print result
		return True
	except socket.herror:
		result = "Unrearchable!"
		print result
		return False

def menu():
	global HOST, PORT
	setup_timeout = 5
	while setup_timeout >0:
		select1 = raw_input("Would you like to setup a different IP Address? (Y/N): ")
		if select1 == 'Y' or select1 == 'y':
			new_ip = raw_input("Please setup your TCP Server IP Address: ")
			if new_ip != "":
				HOST = new_ip
		elif select1 == 'N' or select1 == 'n':
			pass
		else:
			print "Please enter ""Y"" or ""N"" character only."
			setup_timeout -= 1
			continue
				
		select2 = raw_input("Would you like to setup a different Port? (Y/N): ")
		if select2 == "Y" or select2 == "y":
			new_port = raw_input("Please setup your TCP Server Port: ")
			if new_port != "":
				PORT = int(new_port)
				break
			break
		elif select2 == 'N' or select2 == 'n':
			break
		else:
			print "Please enter ""Y"" or ""n"" character only."
			setup_timeout -= 1
			continue
	if setup_timeout == 0:
		print "Timeout, please re-run the program and try carefully!"
		exit(1)


if __name__ == "__main__":
	# Get current IP address
	global HOST, PORT
	HOST = socket.gethostbyname(socket.gethostname())
	PORT = 2365
	print "TCP Server will start on ", HOST,"@",PORT, "..."
	menu()		
	print "TCP Server is running on ", HOST, "@", PORT
	# Activiate
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	# Keep Running
	server.serve_forever()
