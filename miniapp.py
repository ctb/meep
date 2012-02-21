from meep_example_app import MeepExampleApp, initialize
import datatime
import os

def main():
    app = MeepExampleApp()
    environ = {}

    def fake_start_response(status, headers):
        print status
        print headers
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '\n'

    while(True):
        f = raw_input("Enter file name:")
        try:
            f = open(f)
            line = f.readline()
            while line:
                if line.startswith('GET'):
                    line = line.rstrip('\n') #removes extra line
                    words = line.split(' ')
                    environ['REQUEST_METHOD'] = 'GET'
                    environ['PATH_INFO'] = words[1]
                    environ['SERVER_PROTOCOL'] = words[2]
                elif line.startswith('cookie:'):
                    line = line.rstrip('\n') #removes extra line
                    line = line.lstrip('cookie: ') 
                    environ['HTTP_COOKIE'] = line
                line = f.readline()
            app.__call__(environ, fake_start_response)
        except IOError:
            print "Couldn't read that file"


main()
