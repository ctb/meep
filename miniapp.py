from meep_example_app import MeepExampleApp, initialize
import os
import datetime

def main():
    app = MeepExampleApp()
    environ = {}

    def fake_start_response(status, headers):
        print status
        print headers
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '\n'
    

    while(True):
        fileName = raw_input("Give me a text file to read (1-request.txt, 2-request.txt, 3-request.txt)...\n")
        try:
            fp = open(os.getcwd() + "\\requests\\" + fileName) #open cwd gets your current directory

            for line in fp.readlines():
                print line
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

            app.__call__(environ, fake_start_response)
            data = app(environ, fake_start_response)
            print data
        except IOError:
            print "Couldn't read that file"


main()
