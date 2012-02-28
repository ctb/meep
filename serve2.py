
#! /usr/bin/env python
import sys
import socket
import datetime
from meep_example_app import MeepExampleApp, initialize

initialize()
app = MeepExampleApp()
environ = {}
global STATUS
global HEADERS
global TIME
def fake_start_response(status, headers):     # wHat exactly does the fake_start resposne do, somehow it returns the html...
    STATUS=status
    HEADERS=headers
    TIME=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print status
    print headers
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print '\n'

def handle_connection(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                break
            data2=data.splitlines()
            for line in data2:
                print 'data:', (line,)
                if line.startswith('GET'):
                    line = line.rstrip('\n')
                    words = line.split(' ')
                    environ['REQUEST_METHOD'] = 'GET'
                    environ['PATH_INFO'] = words[1]
                    environ['SERVER_PROTOCOL'] = words[2]
                    print "THE GET LINE",line
                elif line.startswith('cookie:'):
                    line = line.rstrip('\n')
                    line = line.lstrip('cookie: ')
                    environ['HTTP_COOKIE'] = line
                    print "THE COOKIE LINE:" ,line

            app.__call__(environ, fake_start_response)
            data = app(environ, fake_start_response)
            #print "DATA[0]",data[0]

            output= "HTTP/1.1 200 0K \r\n Date: Mon, 27, Feb 2012 10:27:15 EST \r\n Server: test/0.1 Python/2.5 \r\n Content-type: text/html \r\n Location: / \r\n "
            datalen=""
            datalen=str(len(data[0]))
            output += "Content-Length: " + datalen +"\r\n\r\n"
            output += data[0]
            print "THE OUTPUT",output
            sock.sendall(output)
            sock.close()

            if '.\r\n' in data:
                sock.close()
                break
        except socket.error:
            break

if __name__ == '__main__':
    interface, port = sys.argv[1:3]
    port = int(port)

    print 'binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)

    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        handle_connection(client_sock)
        print "DONE HANDELING CONNECTION"


###! /usr/bin/env python
##
##import sys
##import socket
##import unittest
##import meep_example_app
##import urllib
##import datetime
##import signal
##
##e = {}
##outputStatus = ''
##outputHeaders = []
##
##def parse_Server_Line(l):
##    global e
##    parts = l.split()
##    e['REQUEST_METHOD'] = parts[0]
##    print "PARTS[0]",parts[0]
##    if len(parts) > 2:
##        e['SERVER_PROTOCOL'] = parts[2]
##        print "PARTS[2]",parts[2]
##    if parts[1].find('?') == -1:
##        e['PATH_INFO'] = parts[1]
##        print "PARTS[1]",parts[1]
##    else:
##        url = parts[1].split('?')
##        e['PATH_INFO'] = url[0]
##        e['QUERY_STRING'] = url[1]
##        print "URL", url
##
##def parse_Content_Type(l):
##    values = l.split(': ')[1]
##    types = values.split(',')
##    e['CONTENT_TYPE'] = types[0]
##
##def parse_Host(l):
##    values = l.split(': ')[1]
##    parts = values.split(':')
##    e['SERVER_NAME'] = parts[0]
##    if len(parts) > 1:
##        e['SERVER_PORT'] = parts[1]
##
##def parse_cookie(l):
##    e['HTTP_COOKIE'] = l.split(': ')[1]
##
##def parse_http_header(l):
##	try:
##		key,value = l.split(': ')
##		key = 'HTTP_%s' % (key.upper().replace('-','_'),)
##		e[key] = value
##	except:
##		pass
##
##def fake_start_response(status, headers):
##	global outputStatus, outputHeaders
##	outputStatus = status
##	outputHeaders = headers
##
##def process_incoming(data,ip,port):
##
##	global e,outputStatus, outputHeaders
##
##	#LOAD DEFAULTS
##	e['SCRIPT_NAME'] = ''
##	e['REQUEST_METHOD'] = 'GET'
##	e['PATH_INFO'] = '/'
##	e['QUERY_STRING'] = ''
##	e['SERVER_PROTOCOL'] = 'HTTP/1.1'
##	e['SERVER_NAME'] = socket.gethostbyaddr("69.59.196.211")
##	e['SERVER_PORT'] = str(port)
##	e['CONTENT_TYPE'] = 'text/plain'
##	e['CONTENT_LENGTH'] = '0'
##	e['HTTP_COOKIE'] = ''
##
##	lines = data.splitlines()
##	for l in lines:
##		if l.startswith('GET'):
##			parse_Server_Line(l)
##			e['CONTENT_LENGTH'] = '0'
##		elif l.lower().startswith('accept:'):
##			parse_Content_Type(l)
##		elif l.lower().startswith('host:'):
##			parse_Host(l)
##		elif l.lower().startswith('cookie'):
##			parse_cookie(l)
##		else:
##			parse_http_header(l)
##
##	print 'processed headers:'
##	for val in e:
##		print '   %s: %s' % (val,e[val],)
##
##	app = meep_example_app.MeepExampleApp()
##	print 'processing'
##	data = app(e, fake_start_response)
##	output = '%s %s\r\n' % (e['SERVER_PROTOCOL'], outputStatus)
##	output += 'Date: %s EST\r\n' % datetime.datetime.now().strftime("%a, %d %b %Y %I:%M:%S")
##	output += 'Server: HaydensAwesomeServer/0.1 Python/2.5\r\n'
##	output += 'Content-type: %s\r\n' % (e['CONTENT_TYPE'],)
##	output += 'Location: %s\r\n' % (e['PATH_INFO'],)
##	if len(data) > 0:
##		output += 'Content-Length: %d\r\n\r\n' % (len(data[0]),)
##		output += data[0]
##	else:
##		output += 'Content-Length: 0\r\n\r\n'
##	print 'done'
##	print "THE OUTPUT", output
##	print "DONT WITH THE OUTPUT"
##	return output
##
##def handle_connection(sock):
##    while 1:
##        try:
##            data = sock.recv(4096)
##            if not data:
##                break
##                    
##            print 'data received from IP: ', (sock.getsockname(),)
##            ip,port = sock.getsockname()
##            sock.sendall(process_incoming(data, ip, port))
##            sock.close()
##            break
##        except socket.error:
##            print 'error'
##            break
##
##if __name__ == '__main__':
##	interface, port = sys.argv[1:3]
##	port = int(port)
##
##
##	print 'binding', interface, port
##	sock = socket.socket()
##	sock.bind( (interface, port) )
##	sock.listen(5)
##
##
##	while 1:
##		print 'waiting...'
##		(client_sock, client_address) = sock.accept()
##		print 'got connection', client_address
##		handle_connection(client_sock)
##
##	sock.close()
