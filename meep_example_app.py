import meeplib
import traceback
import cgi
import meepcookie

from jinja2 import Environment, FileSystemLoader

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)

    # done.

env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

        return [ render_page('index.html', username=username) ]

    def login(self, environ, start_response):
        # hard code the username for now; this should come from Web input!
        username = 'test'

        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]

        cookie_name, cookie_val = \
                     meepcookie.make_set_cookie_header('username',
                                                       user.username)
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

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()

        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return [ render_page('list_messages.html', messages=messages) ]
    
    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return [ render_page('add_message.html') ]

    def add_message_action(self, environ, start_response):
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
                      '/m/add_action': self.add_message_action
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
            print tb
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]
