#! /usr/bin/env python

# See http://docs.python.org/library/xmlrpclib.html

import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:8080/xmlrpc')

print server.hello('woild')

print server.random(10, 20, 5)
