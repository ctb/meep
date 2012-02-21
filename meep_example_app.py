import meeplib
import traceback
import cgi
import pickle
import Cookie
import meepcookie

from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates'))

def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def __init__(self):
    	meeplib.initialize()
        self.username = None

    def userManager(self, environ):
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            return meeplib.get_user(username)
        except:
            return None

    def index(self, environ, start_response):
        print "number of users: %d" %(len(meeplib._users),)
        user = self.userManager(environ)
        start_response("200 OK", [('Content-type', 'text/html')])

        return [ render_page('index.html', user=user) ]

    def login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        print "number of users: %d" %(len(meeplib._users),)

        print "do i have input?", environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        print "form", form

        try:
            username = form['username'].value
            # retrieve user
            print "we gots a username", username
        except KeyError:
            username = ''
            print "no user input"

        try:
            password = form['password'].value
            print "we gots a password", password
        except KeyError:
            password = ''
            print 'no password input'

        s=[]

        ##if we have username and password
        if username != '' and password != '':
            user = meeplib.get_user(username)
            if user is not None and user.password == password:
                ## send back a redirect to '/'
                k = 'Location'
                v = '/'
                headers.append((k, v))
                cookieName, cookieValue = meepcookie.make_set_cookie_header('username', user.username)
                headers.append((cookieName, cookieValue))
                self.username = username
            elif user is None:
                s.append('''Login Failed! <br>
                    The Username you provided does not exist<p>''')

            else:
                ## they messed up the password
                s.append('''Login Failed! <br>
                    The Username or Password you provided was incorrect<p>''')

        ##if we have username or password but not both
        elif username != '' or password != '':
            s.append('''Login Failed! <br>
                    The Username or Password you provided was incorrect<p>''')

        start_response('302 Found', headers)

        ##if we have a valid username and password this is not executed
        s.append('''
                    <form action='login' method='post'>
                        <label>username:</label> <input type='text' name='username' value='%s'> <br>
                        <label>password:</label> <input type='password' name='password'> <br>
                        <input type='submit' name='login button' value='Login'></form>

                        <p><a href='/create_user'>Or Create a New User</a>''' %(username))
        return [''.join(s)]

    def logout(self, environ, start_response):

        self.username =  None

        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        cookieName, cookieValue = \
                    meepcookie.make_set_cookie_header('username', '')
        headers.append((cookieName, cookieValue))
        start_response('302 Found', headers)
        return "no such content"

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        print "do i have input?", environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        print "form", form

        try:
            username = form['username'].value
            # retrieve user
            print "we gots a username", username
        except KeyError:
            username = ''
            print "no user input"

        try:
            password = form['password'].value
            print "we gots a password", password
        except KeyError:
            password = ''
            print 'no password input'

        try:
            password2 = form['password_confirm'].value
            print "we gots a password", password
        except KeyError:
            password2 = ''
            print 'no password confirmation'

        s=[]

        ##if we have username and password and confirmation password
        if username != '':
            user = meeplib.get_user(username)
            ## user already exists
            if user is not None:
                s.append('''Creation Failed! <br>
                    User already exists, please use a different Username<p>''')
            ## user doesn't exist but they messed up the passwords
            elif password == '':
                s.append('''Creation Failed! <br>
                    Please fill in the Password field<p>''')
            elif password != password2:
                s.append('''Creation Failed! <br>
                    The Password and Confirmation Password you provided did not match<p>''')
            else:
                u = meeplib.User(username, password)
                ## send back a redirect to '/'
                k = 'Location'
                v = '/'
                headers.append((k, v))
                self.username = username
        elif password != '' or password2 != '':
            s.append('''Creation Failed! <br>
            Please provide a Username<p>''')


        start_response('302 Found', headers)

        ##if we have a valid username and password this is not executed
        s.append('''
                    <form action='create_user' method='post'>
                        <label>username:</label> <input type='text' name='username' value='%s'> <br>
                        <label>password:</label> <input type='password' name='password' value='%s'> <br>
                        <label>confirm password:</label> <input type='password' name='password_confirm' value='%s'> <br>
                        <input type='submit' name='create user button' value='Create'></form>''' %(username, password, password2))
        return [''.join(s)]

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()
        
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return [ render_page('list_messages.html', messages=messages) ]

    def add_message(self, environ, start_response):
        if self.username is None:
            headers = [('Content-type', 'text/html')]
            start_response("302 Found", headers)
            return [ render_page('add_message_fail.html') ]
        
        headers = [('Content-type', 'text/html')]

        start_response("200 OK", headers)

        return [ render_page('add_message.html') ]
    
    def add_message_action(self, environ, start_response):
        if self.username is None:
            headers = [('Content-type', 'text/html')]
            start_response("302 Found", headers)
            return ["You must be logged in to user this feature <p><a href='/login'>Log in</a><p><a href='/m/list'>Show messages</a>"]


        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        user = self.userManager(environ)

        new_message = meeplib.Message(title, message, user)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)  
        return ["message added"]

    def reply_message_action(self, environ, start_response):
        #Reply Function!!!
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        parent_id = form['parent_id'].value
        reply = form['replymsg'].value
        parent_id = int(parent_id)
        #adds reply to designated message
        message = meeplib.get_message(parent_id)
        message.add_reply(reply)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["reply added"]

    def delete_message_action(self, environ, start_response):
         queryParams = cgi.parse_qs(environ['QUERY_STRING'])
         ID = queryParams['id'][0]
         ID = int(ID)
         meeplib.delete_message(meeplib.get_message(ID))
         
         headers = [('Content-type', 'text/html')]
         headers.append(('Location', '/m/list'))
         start_response("302 Found", headers)
         return ["message deleted"]
    
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
                      '/logout': self.logout,
                      '/create_user': self.create_user,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete_message_action': self.delete_message_action,
                      '/m/reply_message_action': self.reply_message_action
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


#added delete functionality

#added reply functionality 1/23/12

#merged login functionality from hkb261 2/13/12

#Added cookies for users 2/14/12
