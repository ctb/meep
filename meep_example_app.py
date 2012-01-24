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

    def gen_list(self, r, s, d):
        messages = meeplib.get_all_messages()
        for m in messages:
            if (int(m.reply_to) == int(r)):
                s.append('<tr><td>\n')
                s.append("<table border='0'>\n")
                s.append("<tr><td width=%i>\n" % (d*33))
                s.append("\n</td><td width=311 style='background-color: #5eb85e;'>\n")
                s.append('id: %d<br />\n' % (m.id,))
                s.append('title: %s<br />\n' % (m.title))
                s.append('message: %s<br />\n' % (m.post))
                s.append('author: %s<br />\n' % (m.author.username))
                s.append("</td><td style='background-color: #5eb85e;'><table border='0'>\n")
                s.append("<tr><td>\n<form action='del' method='POST'><input type='hidden' name='id' value='%i'><input type='submit' value='delete'></form>\n</td></tr><tr>" % (m.id))
                s.append("<td>\n<form action='add' method='POST'><input type='hidden' name='reply' value='%i'><input type='submit' value='reply'></form>\n</td>" % (m.id))
                s.append('</tr>\n</table>\n</td></tr>\n</table>\n')
                s.append('</td></tr>\n')
                t = self.gen_list(m.id, [], d+1)
                s.append("".join(t))
        return ["".join(s)]


    def list_messages(self, environ, start_response):

        s = ["".join(self.gen_list(-1, ["<table border='0'>\n"], 1))]
        s.append('</table><hr>')
        s.append("<a href='../../'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def del_message(self, environ, start_response):
        # TODO delete all replies to deleted message
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        mid = int(form['id'].value)
        mtd = meeplib.get_message(mid)
        meeplib.delete_message(mtd)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["deleted message"]

    def add_message(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if ('reply' in form):
            reply_id = int(form['reply'].value)
        else:
            reply_id = -1
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        form_code = """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'><input type='hidden' name='reply' value='%i'></form>""" % reply_id
        return form_code

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if ('title' in form):
            title = form['title'].value
        else:
            title = ""

        if ('message' in form):
            message = form['message'].value
        else:
            message = ""

        if ('reply' in form):
            reply = form['reply'].value
        else:
            reply = -1

        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user, reply)

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
                      '/m/del': self.del_message,
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
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]
