from meep_example_app import MeepExampleApp, initialize
import urllib
import os.path
import sys
import datetime
import socket

global status
global header
# function passed to __call__
def fake_start_response(_status, _header):
    global status
    global header
    status = _status
    header = _header

def parse_request(request):
	request.strip()
	lines = request.split('\n')

	# read request
	request = lines.pop(0)
	requestInfo = request.split(' ')
	query = requestInfo[1].split('?')

	form_dict = {}
	
	if requestInfo[0] == "POST":
		print "Cannot handle POST requests currently"

	# process variables
	if len(query) != 1:
	    path_info = query[0]
	    variables = query[1].split('&')
	    for var in variables:
			key,value = var.split('=')
			form_dict[key] = urllib.unquote_plus(value)
	else:
	    path_info = query[0]

	cookie = ''
	for line in lines:
	    tempLine = line.split(':', 2)
	    if tempLine[0] == 'cookie':
		cookie = tempLine[1].strip()

	environ = {} # make a fake request dictionary
	environ['PATH_INFO'] = path_info
	environ['wsgi.input'] = ''
	environ['HTTP_COOKIE'] = cookie
	if len(form_dict):
	    environ['QUERY_STRING'] = urllib.urlencode(form_dict)

	data = app(environ, fake_start_response)

	reply = ""
	reply += "HTTP/1.0 "+status+'\n'
	time = datetime.datetime.now()
	reply += "Date: "+time.strftime("%a, %d %b %Y %H:%M:%S EST")+'\n'
	reply += "Server: WSGIServer/0.1 Python/2.5\n"
	for x in header:
	    key, value = x
	    reply += str(key)+": "+str(value)+'\n'
	if len(data) != 1:
	    reply += 'Content-Length: '+str(len(data))+'\n\n'
	else:
		length = 0
		for x in data:
			length += len(x)
		reply += 'Content-Length: '+str(length)+'\n\n'
	for x in data:
	    reply += str(x)

	return reply

def handle_request(sock):
	while 1:
		try:
			data = sock.recv(4096)
			if not data:
				break
				
			sock.sendall(parse_request(data))
			sock.close()
			break
			
		except socket.error:
			break
			
if __name__ == "__main__":
    app = MeepExampleApp()
    initialize()
    interface = "localhost"
    port = 8000

    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(10)
    print "Serving HTTP on port 8000..."

    while 1:
        try:
            (client_sock, client_address) = sock.accept()
            handle_request(client_sock)
        except KeyboardInterrupt:
            try:
                sock.close()
                sys.exit()
            except:
                sys.exit()
