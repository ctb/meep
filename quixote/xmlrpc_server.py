#!/usr/bin/env python
import quixote
from quixote.publish import Publisher
from quixote.directory import Directory
from quixote.util import xmlrpc

import random

def hello_fn(name):
    return "Hello, %s!" % (name,)

def random_fn(low, high, num):
    "Generate 'num' random integers between 'low' and 'high'"
    x = []
    for i in range(num):
        x.append(random.randint(low, high))

    return x

def process_xmlrpc(fn, params):
    """
    An XML-RPC "dating" function that connects specific functions ('fn')
    and parameters to call the actual function requested.  Could use a
    dict or an object lookup or whatever you wanted here.
    """
    
    if fn == 'hello':
        return hello_fn(*params)
    elif fn == 'random':
        return random_fn(*params)
    
class RootDirectory(Directory):

    _q_exports = ['', 'xmlrpc']

    def _q_index(self):
        return '''These are not the droids you are looking for.'''

    def xmlrpc(self):
        request = quixote.get_request()
        return xmlrpc(request, process_xmlrpc)

def create_publisher():
    return Publisher(RootDirectory(), display_exceptions='plain')


if __name__ == '__main__':
    from quixote.server.simple_server import run
    print 'creating xmlrpc server listening on http://localhost:8080/'
    run(create_publisher, host='localhost', port=8080)
