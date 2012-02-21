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
    meeplib.load()
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
        username="test"

        
        cookie = environ.get("HTTP_COOKIE")
        if cookie is None or (cookie[len('username='):]==''):
				welcome = "You are not logged in"
				return [ render_page('index.html', username="",welcome=welcome) ]
        else:
				welcome = "you are logged in as user:"
				return [ render_page('index.html', username=username,welcome=welcome) ]
        

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
        for result in results:
            s.append(meeplib.get_message(result))
            # replies = meeplib.get_replies(m.id)

            # if (replies!=-1):
                # s.append('<div style="padding-left: 50px;">Replies:</div><br />')
                # for r in replies:
                    
                    # s.append(""" <div style="padding-left: 70px;">&nbsp;%s</div><p>""" % r)

            # s.append('<hr>')
       
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return [ render_page('search_results.html', messages=s) ]
    
    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        return [ render_page('list_messages.html', messages=messages) ]


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
			return [ render_page('add_message.html') ]


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
		return [ render_page('add_reply.html', mId=mId) ]



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
