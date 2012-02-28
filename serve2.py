#! /usr/bin/env python
import sys
import socket
import miniapp
import string

def handle_connection(sock):
    while 1:
        try:
            data = sock.recv(4096)
            if not data:
                break

            response = miniapp.buildResponse(string.split(data, '\r\n'))
            sock.sendall(response)
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