from meep_example_app import MeepExampleApp, initialize
import os
import sys
import datetime

def main():
    app = MeepExampleApp()
    environ = {}

    def fake_start_response(status, headers):
        print status
        print headers
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '\n'

    for arg in sys.argv: # for eery request
        if (arg == sys.argv[0]):
            continue
        f = open(os.getcwd() + "/requests/" + arg)
        for line in f.readlines(): # for eery line in the request
            if line.startswith('GET'):
                line = line.rstrip('\n')
                words = line.split(' ')
                environ['REQUEST_METHOD'] = 'GET'
                environ['PATH_INFO'] = words[1]
                environ['SERVER_PROTOCOL'] = words[2]
            elif line.startswith('cookie:'):
                line = line.rstrip('\n')
                line = line.lstrip('cookie: ')
                environ['HTTP_COOKIE'] = line

        app.__call__(environ, fake_start_response) # respond


main()
