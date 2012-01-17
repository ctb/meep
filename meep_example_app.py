import meeplib
import traceback
import cgi
from cgi import parse_qs, escape #why is this line nescessary!?

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
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

	indexhtml= """
<html>
  <body>
    <p>
	You are logged in as user: %s.
    </p>
    <p>
	<a href='/m/add'>Add a message</a>
    </p>
    <p>
	<a href='/login'>Log in</a>
    </p>
    <p>
	<a href='/logout'>Log out</a>
    </p>
    <p>
	<a href='/m/list'>Show messages</a>
    </p>
  </body>
</html>
	""" % (username,)

        return [indexhtml]

    def login(self, environ, start_response):
        # hard code the username for now; this should come from Web input!
        username = 'test'

        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]
        
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

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
	    deletebutton = '''<form action="delete_action" method="get">\n\t<button name="deleteID" type="submit"value="%s">Delete</button>\n</form>\n''' %(str(m.id,))
	    s.append("<html>\n<body>\n")
            s.append('<p>\n\tid: %d\n</p>\n' % (m.id,))
            s.append('<p>\n\ttitle: %s\n</p>\n' % (m.title))
            s.append('<p>\n\tmessage: %s\n</p>\n' % (m.post))
            s.append('<p>\n\tauthor: %s\n</p>\n' % (m.author.username))
	    s.append(deletebutton)
            s.append('\n<hr>')

        s.append("\n\n<a href='../../'>index</a> \n</body>\n</html>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return """
<html>
  <body>
    <form action='add_action' method='POST'>
    	Title: <input type='text' name='title'><br>
    	Message: <input type='text' name='message'><br>
    	<input type='submit'>
    </form>
  </body>
</html>
	"""

    def delete_message_action(self, environ, start_response):
	qDict = parse_qs(environ['QUERY_STRING'])
	delID = qDict.get('deleteID', [''])[0] #get first item (the only item we need, id of message to be deleted)
	escape(delID) #escape user input, recommended to stop script injection by webpython.codepoint.net
	print delID
	messages = meeplib.get_all_messages()
	for m in messages:
		if int(m.id) is int(delID):
			meeplib.delete_message(m)

	headers = [('Content-type', 'text/html')]
	headers.append(('Location', '/m/list'))
	start_response("302 Found", headers)
	
	return 'message deleted'

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
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
		      '/m/delete_action': self.delete_message_action
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
