import meeplib
import traceback
import cgi
from Cookie import SimpleCookie
import meepcookie
from jinja2 import Environment, FileSystemLoader

def initialize():
    try:
	meeplib.load()
	print "Loading from pickle files"
    except:
	# create a default user
	u = meeplib.User('test', 'foo')
	# create a single message
	meeplib.Message('my title', 'This is my message!', 0, u)
	meeplib.User('new', 'test')
    # done

env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)

def check_cookie(environ):
    try:
	cookie = SimpleCookie()
	cookie.load(environ.get('HTTP_COOKIE'))
	username = cookie['username'].value
	return username
    except:
	return ''

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
	
	username = check_cookie(environ)

        return [ render_page('index.html', username=username) ]

    def login(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        return render_page('login.html')

    def login_action(self, environ, start_response):
	print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

	if "username" not in form or "password" not in form:
	    #If either field is left blank on login, redirect to error page.
	    headers = [('Content-type', 'text/html')] 
            headers.append(('Location', '/invalid_login'))
            start_response('302 Found', headers)
            return "no such content"

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
	    cookie_key, cookie_val = meepcookie.make_set_cookie_header('username', username)

	else:
            #login failed, redirect to error page
	    k = 'Location'
	    v = '/invalid_login'
	    
        # set content-type
        headers = [('Content-type', 'text/html')]
        headers.append((k, v))
	headers.append((cookie_key, cookie_val))
        start_response('302 Found', headers)
        
        return "no such content"

    def invalid_login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
	return render_page('invalid_login.html')

    def logout(self, environ, start_response):
        #Resets username back to '' instead of current user
	cookie_key, cookie_val = meepcookie.make_set_cookie_header('username', '')
        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
	headers.append((cookie_key, cookie_val))
        start_response('302 Found', headers)
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()
        replies = meeplib.get_all_replies()

        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return [render_page('list.html', messages=messages, replies=replies)]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
	username = check_cookie(environ)
	if username == '':
	    #Send to error page if no user is logged in
	    headers.append(('Location', '/m/no_user'))
            start_response("302 found", headers)
	    return "no such content"
	else:
	    start_response("200 OK", headers)
            return render_page('add_message.html')

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        rank = form['rank'].value
        rank = int(rank)
     
	username = check_cookie(environ)
        user = meeplib.get_user(username)
        new_message = meeplib.Message(title, message, rank, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def increase_message_rank(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        msg_id = form['id_num'].value
        msg_id = int(msg_id)
        meeplib.inc_msg_rank(meeplib.get_message(msg_id))

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message upvoted"]

    def decrease_message_rank(self,environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        msg_id = form['id_num'].value
        msg_id = int(msg_id)
        meeplib.dec_msg_rank(meeplib.get_message(msg_id))

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message upvoted"]

    def add_reply(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        headers = [('Content-type', 'text/html')]

	username = check_cookie(environ)
	if username == '':
	    #Send to error page if no user is logged in
	    headers.append(('Location', '/m/no_user'))
            start_response("302 found", headers)
	    return "no such content"
	else:
	    start_response("200 OK", headers)
            id_num = form['id_num'].value
            id_num = int(id_num)
            return render_page('add_reply.html', id_num=id_num)

    def add_reply_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id_num = form['id_num'].value
        id_num = int(id_num)
        reply = form['reply'].value
        rank = form['rank'].value
        rank = int(rank)
        
	username = check_cookie(environ)
        user = meeplib.get_user(username)
        
        new_reply = meeplib.Reply(id_num, reply, rank, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def no_user(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
	return render_page('no_user.html')

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
    
    def increase_reply_rank(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        msg_id = form['id_num'].value
        msg_id = int(msg_id)
        meeplib.inc_reply_rank(meeplib.get_reply(msg_id))

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message upvoted"]

    def decrease_reply_rank(self,environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        msg_id = form['id_num'].value
        msg_id = int(msg_id)
        meeplib.dec_reply_rank(meeplib.get_reply(msg_id))

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message upvoted"]

    def delete_reply_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id_num = form['id_num'].value
        id_number = int(id_num)
        
        meeplib.delete_reply(meeplib.get_reply(id_number))

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["reply deleted"]

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
		      '/m/delete_message': self.delete_message,
		      '/m/no_user': self.no_user,
                      '/m/add_reply': self.add_reply,
                      '/m/add_reply_action': self.add_reply_action,
                      '/m/delete_reply_action': self.delete_reply_action,
                      '/m/increase_msg_rank': self.increase_message_rank,
                      '/m/decrease_msg_rank': self.decrease_message_rank,
                      '/m/increase_reply_rank':self.increase_reply_rank,
                      '/m/decrease_reply_rank':self.decrease_reply_rank
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
