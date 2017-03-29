#!/usr/bin/env python
# TCP Client: Send Message to TCP Server /Python 2.7
# Module is written by Jason/Ge Wu (2nd Verson)
import socket
import sys
import time


class tcp_client:
	apikey = ""
	feedId = ""
	tcp_server = '199.108.99.17'	# Cloud.c2m.net TCP Server
	tcp_port = 3001			# Cloud.c2m.net TCP Server
	buffer_size = 1024		# TCP Message Default Buffer
	status = {}
	c2m_format = True

	def __init__(self, apikey, feedId):
		self.apikey = apikey
		self.feedId = feedId

	def send(self, message):
		if self.apikey.isspace():
			print "invalid C2M apikey!"

		elif self.feedId.isspace():
			print "invalid C2M feedID!"
			if self.status.has_key('error'):
				self.status['error'] += ", invalid feedID"
			else:
				self.status['error'] = "invalid feedID"
		else:
			if self.c2m_format:
				prefix = 'apikey:'+self.apikey+',feedId:'+self.feedId+',feed='
			else:
				prefix = ""
			full_msg = prefix + message
			msg_length = len(full_msg)

			try:
				c2m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				c2m.settimeout(5)			# May need to set different timeout
				c2m.connect((self.tcp_server, self.tcp_port))	
				c2m.send(full_msg)
				print "TCP Message:\n%s" % full_msg
				print "-> Sent time: [ {} ], Length: [{}]".format(
										time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 
										msg_length)

			except socket.timeout:
				print "-> TCP Socket Connection Timeout"
				self.status['send'] = False
				self.status['error'] = "Socket Connection Timeout"
			except socket.error, e:
				print "-> TCP Error Code: %s" % e[0]
				self.status['send'] = False
				self.status['error'] = e[1]
			else:
				self.status['send'] = True
			finally:
				c2m.close()
				return self.status

	# receive() method is an example, should be modified into send() within one socket connection
	def receive(self):
		try:
			c2m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			c2m.connect((self.tcp_server, self.tcp_port))
			receive_msg = c2m.recv(self.buffer_size)
			msg_length = len(receive_msg)
			if msg_length >= self.buffer_size-1:
				print "-> Received message reached the MAX size of the buffer!"
				self.buffer_size = self.buffer_size * 2
			else:
				pass

			print "-> [ {} ], Length [{}]".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),msg_length)
			print "Received:\n%s" % receive_msg

		except socket.error, e:
			print "-> TCP Error : %s" % e[0]
			self.status['receive'] = False
			self.status['error_code'] = e[1]
			return self.status
		else:
			c2m.close()
			self.status['receive'] = True
			return self.status

def main():
	HOST = raw_input("Please enter New TCP Server Address: ")
	PORT = raw_input("Please enter New TCP Server Port: ")
	c2m = tcp_client("", "")

	if HOST != "" and (not HOST.isspace()):
		print "check IP"
		c2m.tcp_server = HOST

	if PORT != "" and PORT.isdigit():
		print "check port"
		c2m.tcp_port = int(PORT)

	c2m.c2m_format = False
	MSG = raw_input("Please enter your Message: ")

	check = c2m.send(MSG)
	print check

if __name__ == '__main__':
	main()