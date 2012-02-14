import meeplib
import traceback
import cgi
import meepcookie

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)
    meeplib.load()
    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        username="test"

        
        cookie = environ.get("HTTP_COOKIE")
        if cookie is None or (cookie[len('username='):]==''):
            return ["""you are not logged in<p><a href='/login'>Log in</a><p><a href='/m/list'>Show messages</a>"""]
        else:
            return ["""you are logged in as user: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]
  
        

    def login(self, environ, start_response):
        # hard code the username for now; this should come from Web input!
        username = 'test'

        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]
        #cookies
        cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',user.username)

        headers.append((cookie_name, cookie_val))
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]
        cookie_name, cookie_val = meepcookie.make_set_cookie_header('username','')

        headers.append((cookie_name, cookie_val))
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"
    
    def list_search(self, environ, start_response):
        results=meeplib.get_search_results()
        s = []
        s.append('Your Search Results')
        s.append('<hr>')
        print "RESULTS"
        print results
        for result in results:
            m=meeplib.get_message(result)
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            try:
                s.append('author: %s<p>' % (m.author.username))
            except:
                s.append('author: %s<p>' % (m.author))
            s.append("<a href='/m/add_reply?id="+str(m.id)+"'>Reply</a><br />")
            s.append("<a href='/m/delete_message?id="+str(m.id)+"'>Delete Message</a>")
            replies = meeplib.get_replies(m.id)

            if (replies!=-1):
                s.append('<div style="padding-left: 50px;">Replies:</div><br />')
                for r in replies:
                    
                    s.append(""" <div style="padding-left: 70px;">&nbsp;%s</div><p>""" % r)

            s.append('<hr>')
       
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        s.append("<form action='search_action' method='POST'>Search<input type='text' name='text'><input type='submit'></form>")

        return ["".join(s)]
    
    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()
        s = []
        for m in messages:
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message:<b> %s</b><p>' % (m.post))
            try:
                s.append('author: %s<p>' % (m.author.username))
            except:
                s.append('author: %s<p>' % (m.author))
            s.append("<a href='/m/add_reply?id="+str(m.id)+"'>Reply</a><br />")
            s.append("<a href='/m/delete_message?id="+str(m.id)+"'>Delete Message</a>")
            replies = meeplib.get_replies(m.id)
            if (replies!=-1):
                s.append('<div style="padding-left: 50px;">Replies:</div><br />')
                for r in replies:
                    
                    s.append(""" <div style="padding-left: 70px;">&nbsp;%s</div><p>""" % r)

            s.append('<hr>')

        s.append("<a href='../../'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        s.append("<form action='search_action' method='POST'>Search<input type='text' name='text'><input type='submit'></form>")

        return ["".join(s)]


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

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)
        meeplib.save_message()
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_message(self, environ, start_response):
        qString = cgi.parse_qs(environ['QUERY_STRING'])
        mId = qString.get('id', [''])[0]
        messageID = meeplib.get_message(int(mId))
        meeplib.delete_message(messageID)
   
     
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        
        return ["message deleted"]



    def add_reply(self, environ, start_response):
        qString = cgi.parse_qs(environ['QUERY_STRING'])
        mId = qString.get('id', [''])[0]
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        return """<form action='add_reply_action' method='POST'><input type='hidden' name='id' value='%s'><br>Message:<input type='text' name='message'><br><input type='submit'></form>""" %mId


    def add_reply_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        message = form['message'].value
        mId = int(form['id'].value)
        
        meeplib.add_reply(mId, message)
        meeplib.save_reply()
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        
        return ["Replied"]
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete_message': self.delete_message,
                      '/m/add_reply': self.add_reply,
                      '/m/add_reply_action':self.add_reply_action,
                      '/m/search_action': self.search_message_action,
                      '/m/search': self.list_search
                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found."]

        try:
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]
