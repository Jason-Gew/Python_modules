#!/usr/bin/env python
#
import BaseHTTPServer
import socket
import base64
import time
import sys

HOST_URL = ""
HOST_PORT = 8888

response_code = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        }


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def _headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_HEAD(self):
		self._headers()

	def do_GET(self):
		"""Respond to a GET request."""
		self._headers()
		self.wfile.write("<html><head><title>Jason/Gew</title></head>")

		self.wfile.write("<body><p style=font-family:verdana;><b>+-------------------------  Welcome  ------------------------+</b></p>")
		system_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		self.wfile.write("<p style=color:blue;> Your Visit Time: "+system_time+"</p>")
		self.wfile.write("<p>Your path: %s</p>" % self.path)
		self.wfile.write("</body></html>")


	def do_POST(self):
		self._headers()
		print "-> POST:" 
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		self.send_response(200)
		self.end_headers()
		# Data Parser/handler
		data = self.data_string
		print data
'''
	def address_string(self):
		host, port = self.client_address[:2]
		return socket.getfqdn(host)
'''
if __name__ == '__main__':
	print "\n+--------------------  Intialize  -------------------+"
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_URL, HOST_PORT), MyHandler)
	print "[{}] HTTP Server Running on {} @ {}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),HOST_URL,HOST_PORT)
	try:
		httpd.serve_forever()

	except KeyboardInterrupt:
		print "[{}] HOST Terminated!\n".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

	httpd.server_close()
	print "+------------------------  End  -----------------------+"