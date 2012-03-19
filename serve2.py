
#! /usr/bin/env python
import sys
import socket
import datetime
from meep_example_app import MeepExampleApp, initialize

initialize()
app = MeepExampleApp()
environ = {}
STATUS=""
HEADERS=""
TIME=""
COOKIE=""
def fake_start_response(status, headers):     # wHat exactly does the fake_start resposne do, somehow it returns the html...

    STATUS=status
    HEADERS=headers                  #the cookie is right in here, how do i send that to index
    TIME=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print "STATUS",status
    print "HEADERS",headers
   # environ['HTTP_COOKIE'] = "USER"
    print len(headers)
    for header in headers:
        print header[0], "SPACE", header[1]
        if header[0]=="Set-Cookie":
            cookie=header[1]
          #  print "COOKIE BEFORE I MESS WITH IT", cookie
            cookielist=cookie.split(";")       #  "WONT WORK IF SOMEONES NAME HAS A :"
          #  print "list",cookielist
            cookie=cookielist[0]
           
            environ['HTTP_COOKIE'] = cookie
        #    print "SET THE COOKIE", cookie
            
##    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
##    print '\n'
    #whats going on in here?

def handle_connection(sock):

    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                break
            data2=data.splitlines()
            print 'data: What the Socket Recieves \n\n',
            for line in data2:
                print line
                if line.startswith('GET'):
                    line = line.rstrip('\n')
                    words = line.split(' ')
                    environ['REQUEST_METHOD'] = 'GET'
                    environ['PATH_INFO'] = words[1]
                    environ['SERVER_PROTOCOL'] = words[2]
                  #  print "THE GET LINE",line
                elif line.startswith('Cookie: '):
                    line = line.rstrip('\n')
                    line = line.lstrip('Cookie: ')
                   # environ['HTTP_COOKIE'] = line
                  #  print "THE COOKIE LINE:" ,line
           # print "SETTING ENVIRON COOKIE",COOKIE
           # environ['HTTP_COOKIE'] = "username=USER"
            print "Environ\n",environ                            # should pathinfo contain only /m/addaction or should it contain the message and stuff too +rerouting


            print "FAKE RESPONSE", fake_start_response

          
            app.__call__(environ, fake_start_response)          # routes us to the right place in meep example app?

            
            data = app(environ, fake_start_response)             #so the problem is before we get the data






           
            #print "DATA[0]",data[0]
       #     print "HEADERS", HEADERS
            output= "HTTP/1.1 "+ STATUS +"\r\n Date: "+TIME+ "\r\n Server: test/0.1 Python/2.5 \r\n Content-type: text/html \r\n Location: / \r\n "
            datalen=""
            datalen=str(len(data[0]))
            output += "Content-Length: " + datalen +"\r\n\r\n"
            output += data[0]                                           # the data being sent for the bad links is page not found
            
            print "THE OUTPUT \n\n",output
            print "DATA[0] \n\n",data[0]
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


