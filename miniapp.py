from meep_example_app import MeepExampleApp, initialize
import urllib
import os.path
import sys
import datetime

global status
global header
# function passed to __call__
def fake_start_response(_status, _header):
    global status
    global header
    status = _status
    header = _header

argList = []

for arg in sys.argv:
	argList.append(arg)

# remove script pathname
argList = argList[1:]

if argList:
    path = argList.pop(0)
    fullpath = os.path.abspath(path)
else:
    path = raw_input("Specify a path name:")
    fullpath = os.path.abspath(path)

try:
    f = open(fullpath, 'r')
except:
    print fullpath, " does not exist. Exiting."
    sys.exit()

lines = []
for line in f.readlines():
    lines.append(line.strip())
f.close()

# read request
request = lines.pop(0)
requestInfo = request.split(' ')
query = requestInfo[1].split('?')

form_dict = {}

# process variables
if len(query) != 1:
    path_info = query[0]
    variables = query[1].split('&')
    for var in variables:
	key,value = var.split('=')
	form_dict[key] = urllib.unquote_plus(value)
else:
    path_info = query[0]

cookie = ''
for line in lines:
    tempLine = line.split(':', 2)
    if tempLine[0] == 'cookie':
        cookie = tempLine[1].strip()

environ = {} # make a fake request dictionary
environ['PATH_INFO'] = path_info
environ['wsgi.input'] = ''
environ['HTTP_COOKIE'] = cookie
if len(form_dict):
    environ['QUERY_STRING'] = urllib.urlencode(form_dict)

initialize()
app = MeepExampleApp()

data = app(environ, fake_start_response)

fileToWrite = raw_input("File to write to: ")
fullpath = os.path.abspath(fileToWrite)
f = open(fullpath, 'w')
f.write("HTTP/1.0 "+status+'\n')
time = datetime.datetime.now()
f.write("Date: "+time.strftime("%a, %d %b %Y %H:%M:%S EST")+'\n')
f.write("Server: WSGIServer/0.1 Python/2.5\n")
for x in header:
    key, value = x
    f.write(str(key)+": "+str(value)+'\n')
if len(data) != 1:
    f.write('Content-Length: '+str(len(data))+'\n\n')
else:
    length = 0
    for x in data:
	length += len(x)
    f.write('Content-Length: '+str(length)+'\n\n')
for x in data:
    f.write(str(x))

f.close()
