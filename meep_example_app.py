import meeplib
import traceback
import cgi


def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
		username = 'test'
	
		start_response("200 OK", [('Content-type', 'text/html')])
		return ["""You are not logged in, please login below.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a><p>"""]

    def login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='login_action' method='POST'>Username: <input type='text' name='user'><br>Password:<input type='text' name='pass'><br><input type='submit'></form>"""

    def login_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        username = form['user'].value
        password = form['pass'].value
	
	headers = [('Content-type', 'text/html')]
	print password
	print username
	if(password == "admin"):
		print 'here'
		start_response("302 Found", headers) 
		return ["""You are logged in as %s<p><a href='/m/add'>Add a message</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a><p>"""% (username,)]
	else:
		print 'not here'
		start_response("302 Found", headers)  
		return ["""Authentication Failed, please try again<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a><p>"""]


    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()

        s = []
        for m in messages:
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
            s.append("<div style='text-align:right'><form action='delete' method='POST'><input type='hidden' name='id' value='%i'><input type='submit' value='delete message'></form></div>"%m.id)
            s.append('<hr>')

        s.append("<a href='../../'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

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

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)  
        return ["message added"]
    
    def delete_message(self,environ,start_response):
    
    	form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        id= form['id'].value   
        mes = meeplib.get_all_messages()
     	for m in mes:
				if(m.id == int(id)):
					meeplib.delete_message(m)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 OK", headers)
        #print id
        return ["message deleted"]
        
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
					 # '/success':self.success,
					 #'/failure':self.failure,
					  '/login_action':self.login_message_action,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete':self.delete_message
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
