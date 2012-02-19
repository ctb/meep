from meep_example_app import MeepExampleApp, initialize
import urllib
import os.path
import sys
import datetime

global _status
global _headers
# the function we will use to pass to __call__
def fake_start_response(status, headers):
    global _status
    global _headers
    _status = status
    _headers = headers

argList = []

for arg in sys.argv:
	argList.append(arg)
	
# remove script path
argList = argList[1:]

if argList:
    filepath = argList.pop(0)
    filepath = os.path.abspath(filepath)
else:
    filepath = raw_input("Specify a filepath, can be absolute or relative: ")
    filepath = os.path.abspath(filepath)

try:
    fh = open(filepath, 'r')
except:
    print filepath,
    print "is not readable or does not exist. Exiting."
    sys.exit()

allLines = []
for line in fh.readlines():
    allLines.append(line.strip())
fh.close()

# read request line
request = allLines.pop(0)
# split on whitespace
requestInfoList = request.split(' ')
#print requestInfoList

fullQueryList = requestInfoList[1].split('?')
#print fullQueryList

form_dict = {}

# no variables to get
if len(fullQueryList) == 1:
    path_info = fullQueryList[0]
# we need to do further processing on the variables
else:
    path_info = fullQueryList[0]
    tmpVariables = fullQueryList[1].split('&')
    for variablePair in tmpVariables:
        key,value = variablePair.split('=')
        form_dict[key] = urllib.unquote_plus(value)

#print allLines

cookie = ''
# get the cookie
for line in allLines:
    tmp = line.split(':', 2)
    if tmp[0] == 'cookie':
        cookie = tmp[1].strip()

#print 'cookie = ', cookie

environ = {} # make a fake request dictionary
environ['PATH_INFO'] = path_info
environ['wsgi.input'] = ''
environ['HTTP_COOKIE'] = cookie
if len(form_dict):
    environ['QUERY_STRING'] = urllib.urlencode(form_dict)

initialize()
app = MeepExampleApp()

#print environ
data = app(environ, fake_start_response)

#print _status
#print _headers

#print data

print "HTTP/1.0", _status
now = datetime.datetime.now()
print "Date:", now.strftime("%a, %d %b %Y %H:%M:%S EST")
print "Server: WSGIServer/0.1 Python/2.5"
for x in _headers:
    print x
print
for x in data:
    print x
