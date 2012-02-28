#! /usr/bin/env python
import sys
import socket
from meep_example_app import MeepExampleApp, initialize
import datetime
initialize()
app = MeepExampleApp()
app.override_authentication = True

def handle_connection(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                break

            print 'Data:', (data,)

            def fake_start_response(status, headers):
                print status
                print headers
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                print '\n'
    
            environ = {}
            environ['PATH_INFO'] = data.lstrip('GET').strip()
            for x in app.__call__(environ, fake_start_response):
                sock.sendall(x)

            if '.\r\n' in data:
                sock.close()
                break
        except socket.error:
            break

if __name__ == '__main__':
    interface, port = sys.argv[1:3]
    port = int(port)
    

    print 'Binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)

    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        handle_connection(client_sock)
