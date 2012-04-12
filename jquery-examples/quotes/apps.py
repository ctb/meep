import os
import jinja2
import os.path
import mimetypes
import traceback
import random

class QuotesApp(object):
   def __init__(self, quotes_file, files_path):
      self.quotes = open(quotes_file).readlines()
      self.quotes = [ x.strip() for x in self.quotes ] # remove whitespace
      
      self.file_server = FileServer(files_path)

   def __call__(self, environ, start_response):
      url = environ['PATH_INFO']
      print 'requested URL is:', url
      if url == '/generate_quote':
         quote = random.choice(self.quotes)

         start_response("200 OK", [('Content-type', 'text/html')])
         return quote

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
