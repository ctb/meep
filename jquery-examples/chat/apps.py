import os
import os.path
import mimetypes
import traceback
import random
import time
import cgi

class Message(object):
   def __init__(self, timestamp, user, message):
      self.timestamp = timestamp
      self.user = user
      self.message = message

class ChatApp(object):
   def __init__(self, files_path):
      self.file_server = FileServer(files_path)
      self.messages = []
   
   def get_messages_since(self, timestamp):
      """Retrieve any messages received since the given timestamp."""
      x = []
      for m in self.messages:
         if m.timestamp > timestamp:
            x.append(m)

      return x

   def format_response(self, new_messages, timestamp):
      x = []
      for m in new_messages:
         x.append("""\
<message>
 <author>%s</author>
 <text>%s</text>
</message>
""" % (m.user, m.message))

      if x:                             # new messages received?
         # yes
         status = 1
      else:
         status = 2                     # no new messages

      xml = """
<?xml version="1.0"?>
<response>
 <status>%d</status>
 <time>%f</time>
%s
</response>
""" % (status, timestamp, "".join(x))

      return xml

   def __call__(self, environ, start_response):
      url = environ['PATH_INFO']
      if url == '/get_messages':
         # last_time
         form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
         last_time = float(form['last_time'].value)

         new_messages = self.get_messages_since(last_time)
         xml = self.format_response(new_messages, time.time())

         # done; return whatever we've got.
         start_response("200 OK", [('Content-type', 'text/html')])
         
         print xml
         return [xml]
      elif url == '/post_message':
         form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

         # retrieve submitted data
         last_time = float(form['last_time'].value)
         author = form['user'].value
         message = form['message'].value

         # create and add new message:
         timestamp = time.time()
         m = Message(timestamp, author, message)
         self.messages.append(m)

         # return any new messages:
         new_messages = self.get_messages_since(last_time)
         xml = self.format_response(new_messages, timestamp)

         # done; return whatever we've got.
         start_response("200 OK", [('Content-type', 'text/html')])
         
         print xml
         return [xml]

      # by default, just return a file
      return self.file_server(environ, start_response)

class FileServer(object):
   def __init__(self,path):
      self.path = os.path.abspath(path)
   
   def __call__(self, environ, start_response):
      url = environ['PATH_INFO']
      
      print 'url:' + url
      if url.endswith('/'):
          url += 'index.html'
          
      fullpath = self.path + url
      fullpath = os.path.abspath(fullpath)
      assert fullpath.startswith(self.path)
      
      extension=mimetypes.guess_type(fullpath)
      extension=extension[0]
      
      if extension is None:
          extension = 'text/plain'
     
      status = '200 OK'
      headers = [('Content-type', extension )]
      
      try:
        fp = open(fullpath)
        contents = fp.read()
        start_response(status, headers)
        return [contents]
      except:
        status = '404 Not Found'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        return ['404 Not Found']
