import meeplib
import traceback
import cgi
import meepcookie

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)
def initialize():
   
   # try:
    #meeplib.saveUSER('test','foo',meeplib._get_next_user_id())
    #u = meeplib.User('test', 'foo',-1)
    #meeplib.loadUSER()
   
   # except:
       # print "NO FILE"
    # create a default user
    

    # create a single message
  #  meeplib.Message('my title', 'This is my message NOW!', u,-1)
   # meeplib.Message('title', 'lol', u,-1)
    #meeplib.Message('my', 'test', u,-1)
   # meeplib.Message('test', 'my', u,-1)
    try:
        meeplib.load()
    except:
        print "did not load"
    # done.
   # print "No Initiialize"
    print "INITIALIZED /n/n/n/n YES"

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    
      
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        #check cookie to find a  user, if nto set blank username
       # print "Username", username, len(username)


        cookie = environ.get("HTTP_COOKIE")
      #  print "YUMMY COOKIES \n\n\n", cookie, environ
        if cookie is None or len(cookie)==9:
            print "NO USERNAME COOKIE"
            username2 = ''
            loggedInMessage="Not Logged IN"
        else:
        #    print len('username=')
            username2 = cookie[9:]
        #    print "USERNAME\n", username2,
            loggedInMessage = 'You are logged in as user: %s' % (username2,)
        if username2=='':
        #    print "USERNAME IS BLANK"
            return [ render_page('index.html', username="NONE") ]
            #return ["""you are not logged in %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a><p><p><a href='/m/IDTEST'>Get next User ID</a><p>""" % (username,)]
        else:
            #return ["""you are logged in as user: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a><p><p><a href='/m/IDTEST'>Get next User ID</a><p>""" % (username,)]
            return [ render_page('index.html', username=username2) ]

    def login(self, environ, start_response):
        
        print "IN LOGIN \n\n\n"
        print "Environ:", environ, "start+response", start_response
        # hard code the username for now; this should come from Web input!
        username = 'test'
        u = meeplib.User('test', 'foo',-1)
        # retrieve user
        user = meeplib.get_user(username)
        print "User", user
        # set content-type
        headers = [('Content-type', 'text/html')]
        cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',user.username)

        headers.append((cookie_name, cookie_val))
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        print "HEADERS INSIDE OF LOGIN \n\n"
        print headers
        
        return "no such content"

    def logout(self, environ, start_response):

        headers = [('Content-type', 'text/html')]
        cookie_name, cookie_val = meepcookie.make_set_cookie_header('username','')

        headers.append((cookie_name, cookie_val))
        
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        
        start_response('302 Found', headers)
        print "HEADERS INSIDE OF LOGOUT \n\n"
        print headers
        return "no such content"
    def list_search(self, environ, start_response):
   #     print "ENVIRON", environ
        results=meeplib.get_search_results()
        s = []

        print "RESULTS"
        print results 
        for result in results:
            s.append(meeplib.get_message(result))
##          m=meeplib.get_message(result)
##            s.append('id: %d<p>' % (m.id,))
##            s.append('title: %s<p>' % (m.title))
##            s.append('message: %s<p>' % (m.post))
##            try:
##                s.append('author: %s<p>' % (m.author.username))
##            except:
##                s.append('author: %s<p>' % (m.author))
##            s.append("<a href='/m/post_reply?id="+str(m.id)+"'>Reply</a><p>")
##            if meeplib.has_replies(m.id):
##                s.append('<dd>Replies:<hr />')
##                for r in meeplib.get_replies(m.id):
##                    s.append('<dd>%s<p>' % (r))
##                s.append('</dd>')
##
##            s.append('<hr>')
       
         #TODO MAKE IT DO SEARCH
      #  s.append("<form action='delete_action' method='POST'>Delete a Message?<br> Message ID: <input type='text' name='id'><input type='submit'>Delete</form>")    
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
       # s.append("<form action='search_action' method='POST'>Search for Messages?<br> Message ID: <input type='text' name='text'><input type='submit'>Delete</form>")    
        return [ render_page('search_messages.html', messages=s, meeplib=meeplib) ]

        return ["".join(s)]



        
    def list_messages(self, environ, start_response):


        messages = meeplib.get_all_messages()

##        s = []
##        s.append('<hr>')
##        for m in messages:
##            print m.id
##            s.append('id: %d<p>' % (m.id,))
##            s.append('title: %s<p>' % (m.title))
##            s.append('message: %s<p>' % (m.post))
##            print "M",m
##            try:
##                s.append('author: %s<p>' % (m.author.username))
##            except:
##                s.append('author: %s<p>' % (m.author))
##         
## 
##           
##
##
##            s.append("<a href='/m/post_reply?id="+str(m.id)+"'>Reply</a><p>")
##            if meeplib.has_replies(m.id):
##                s.append('<dd>Replies:<hr />')
##                for r in meeplib.get_replies(m.id):
##                    s.append('<dd>%s<p>' % (r))
##                s.append('</dd>')
##               
##        s.append('<hr>')


       # s.append("<form action='delete_action' method='POST'>Delete a Message?<br> Message ID: <input type='text' name='id'><input type='submit'>Delete</form>")    
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        #s.append("<form action='search_action' method='POST'>Search for Messages?<br> Message ID: <input type='text' name='text'><input type='submit'>Delete</form>")    
        return [ render_page('list_messages.html', messages=messages, meeplib=meeplib) ]
    #TODO MAKE IT SHOW REPLIES
        #return ["".join(s)]

    def add_message(self, environ, start_response):
        print "IN ADD MESSAGE"
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

       # return """<form action='add_action' method='GET'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""
        return [ render_page('add_message.html') ]
##    def search (self, environ, start_response):
##     
##        headers = [('Content-type', 'text/html')]
##        start_response("200 OK", headers)
##
##        return """<form action='search_action' method='POST'>Message:<input type='text' name='id'><br><input type='submit'></form>"""
##
    def search_message_action(self, environ, start_response):
        print "searchaction"
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        text=form['text'].value
    
        searchlist=meeplib.search_message_dict(text)
       

        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/search'))
        start_response("302 Found", headers)
        

        return ["message deleted"]















    
    ############################
    def delete_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return """<form action='delete_action' method='POST'>Message:<input type='text' name='message'><br><input type='submit'></form>"""
    
    def delete_message_action(self, environ, start_response):
        print "deleteaction"
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        message=int(form['id'].value)
        messages = meeplib.get_all_messages()
      #  meeplib.delete_message(messages[0])
        meeplib.delete_message(messages[message])
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        return ["message deleted"]
    
    ###############################


        
    def add_message_action(self, environ, start_response):
        print "TRYING TO ADD A MESSAGE!!!!\n"
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
       
        title = form['title'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        msgid=meeplib._get_next_message_id()
       
        new_message = meeplib.Message(title, message, user,-1)
        meeplib.saveMSG()
        #meeplib.delete_message(new_message)
  
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def add_reply_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        print form
        reply = form['reply'].value
        mId = form['message_id'].value
        
        meeplib.add_reply(int(mId), reply)
        meeplib.saveREPLY()
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["reply added"]

    def delete_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        return """<form action='delete_action' method='POST'>id: <input type='text' name='id'><br><input type='submit'></form>"""

    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id = int(form['id'].value)
        print id, ' A';
        meeplib.delete_message(meeplib.get_message(id))
        meeplib.delete_reply(id)
        meeplib.saveMSG()
        meeplib.saveREPLY()
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/'))
        start_response("302 Found", headers)
        return ["message deleted"]
    
    def IDTEST (self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

      #  id = int(form['id'].value)
      #  print id, ' A';
        meeplib._get_next_user_id()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/'))
        start_response("302 Found", headers)
        return ["message deleted"]
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/search': self.list_search,
                      '/m/add': self.add_message,

                      '/m/add_action': self.add_message_action,
                      '/m/delete': self.delete_message,
                      '/m/delete_action': self.delete_message_action,
                      '/m/search_action': self.search_message_action,

		            
                      '/m/post_reply' : self.post_reply,
                      '/m/add_reply_action' : self.add_reply_action,
                      '/m/IDTEST' : self.IDTEST,

                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found." + repr(url) ]

        try:
            print "FN", fn
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)
            print "FN", fn
            print "X", x
            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]

    def post_reply(self, environ, start_response):
        #Get message id
        qString = cgi.parse_qs(environ['QUERY_STRING'])
        mId = qString.get('id', [''])[0]

        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        #brownie points below
        x = """<form action='add_reply_action' method='POST'><input type='hidden' value='%s' name='message_id'>Reply:<input type='text' name='reply'><input type='submit'></form>""" % (mId)
        return x
