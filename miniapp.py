import datetime
import sys
import urllib
from meep_example_app import MeepExampleApp, initialize

global _status
global _headers
def fake_start_response(status, headers):
    global _status
    global _headers
    _status = status
    _headers = headers
    
environMap = {
        #REQUEST_METHOD / PATH_INFO will be parsed out in buildResponse
        'accept-language' : 'HTTP_ACCEPT_LANGUAGE',
        'accept-connection' : 'HTTP_CONNECTION',
        'accept' : 'HTTP_ACCEPT',
        'user-agent' : 'HTTP_USER_AGENT',
        'accept-charset' : 'HTTP_ACCEPT_CHARSET',
        'host' : 'HTTP_HOST',
        'referer' : 'HTTP_REFERER',
        #'cache-control' : ?, #can't find this variable
        'cookie' : 'HTTP_COOKIE',
        'accept-encoding' : 'HTTP_ACCEPT_ENCODING'
       }

def buildResponse(webRequest):
    
    #parse request
    requestMap = {'wsgi.input' : ''}
    
    for line in webRequest:
        line = line.strip() #remove leading and trailing whitespace
        
        if (line.startswith('GET') or 
            line.startswith('POST')):
            line = line.split()
            requestMap['REQUEST_METHOD'] = line[0]
            if line[1].find('?') == -1:
                requestMap['PATH_INFO'] = line[1]
            else:
                tmpPath = line[1].split('?')
                requestMap['PATH_INFO'] = tmpPath[0]
                requestMap['QUERY_STRING'] = tmpPath[1]

        else:
            try:
                line = line.split(':',1)
                requestMap[environMap[line[0].lower()]] = line[1].strip()
            except:
                pass
    
    #build response
    initialize()
    app = MeepExampleApp()
    response = app(requestMap, fake_start_response)
    output = []
    output.append('HTTP/1.0 ' + _status)
    currentTime = datetime.datetime.now()
    output.append('Date: ' + currentTime.strftime('%a, %d %b %Y %H:%M:%S EST'))
    output.append('Server: WSGIServer/0.1 Python/2.5')
    for tmpHeader in _headers:
        output.append(tmpHeader[0] + ': ' + tmpHeader[1])
    output.append('\r\n')
    for r in response:
        output.append(r)
    return '\r\n'.join(output)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: miniapp <input file> <output file>"
    else:
        try:
            inFile = open(sys.argv[1], 'r')
            request = inFile.readlines()
            inFile.close()
        except:
            print "Cannot find input file"
        outFile = open(sys.argv[2], 'w')
        outFile.write(buildResponse(request))
        outFile.close()
        
        
    