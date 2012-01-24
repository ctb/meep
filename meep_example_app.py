import meeplib
import traceback
import cgi

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)
    meeplib.User('new', 'test')

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    global username
    username = ''
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
	
	global username

        return ["""you are logged in as user: %s<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]

    def login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='login_action' method='POST'>Username: <input type='text' name='username'><br>Password: <input type='password' name='password'><br><input type='submit'></form>"""

    def login_action(self, environ, start_response):
	print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)	
	
	global username
	tryuser = form['username'].value
	trypass = form['password'].value
	login_success = False

	users = meeplib.get_all_users()
	for u in users:
	    if u.username == tryuser:
		if u.password == trypass:
		    username = tryuser
		    login_success = True
	if login_success:
	    #login successful, redirect to index
	    k = 'Location'
	    v = '/'
	else:
            #login failed, redirect to error page
	    k = 'Location'
	    v = '/invalid_login'
	    
        # set content-type
        headers = [('Content-type', 'text/html')]
        
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def invalid_login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
	return """Invalid username or password<p>
		<a href='/login'>Retry Login?</a><p>
		<a href='../../'>Back to Home</a>"""

    def logout(self, environ, start_response):
        #Resets username back to '' instead of current user
	global username
	username = ''
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
            s.append('id: %d<p>' % (m.id))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
	    s.append('<form action="delete_message" method="POST"><input type="hidden" name="id" value="%d"><input type="submit" value="Delete Message"></form>' % (m.id))
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
	global username

        title = form['title'].value
        message = form['message'].value
        
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_message(self, environ, start_response):
	print environ['wsgi.input']
	form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

	# Get the message id from form, convert to int
	id = int(form['id'].value)
	
	# Get message using built in function, delete the message
	message = meeplib.get_message(id)
	meeplib.delete_message(message)

	headers = [('Content-type', 'text/html')]
	headers.append(('Location', '/m/list'))
	start_response("302 Found", headers)
	return ["message deleted"]
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
		      '/login_action': self.login_action,
		      '/invalid_login': self.invalid_login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
		      '/m/delete_message': self.delete_message
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
