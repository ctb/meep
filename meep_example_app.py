import meeplib
import traceback
import cgi

def initialize():
    # create a default user with username: test, password: test
    u = meeplib.User('test', 'test')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'Not Logged in'

        return ["""Login or <a href='/create_user'>Create an Account</a>

</br><p><form action='login' method='POST'>
Username: <input type='text' name='username'><br>
Password:<input type='password' name='password'><br>
<input type='submit' value='Login'></p></form>

"""]

    def main_page(self, environ, start_response):
        try:
            meeplib.get_curr_user()
        except NameError:
            meeplib.delete_curr_user()
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        username = meeplib.get_curr_user()

        return ["""You have successfully logged in as: %s <p><a href='/m/add'>Add a message</a><p><p><a href='/m/messages'>Show messages</a><p><a href='/logout'>Log out</a>""" % (username,)]

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("302 Found", headers)
        return """Enter your username and password: <p><form action='create_user_action' method='POST'>
Username: <input type='text' name='username'><br>
Password:<input type='password' name='password'><br>
<input type='submit' value='Create User'></form</p>"""

    def create_user_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #TODO Error Checking on Creating a User
        returnStatement = "user added"
       
        username = form['username'].value
        password = form['password'].value
  
        new_user = meeplib.User(username, password)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/'))
        start_response("302 Found", headers)

        return [returnStatement]

    def login(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        username = form['username'].value
        password = form['password'].value

        # Test whether variable is defined to be None
        if username is not None:
             if password is not None:
                 if meeplib.check_user(username, password) is False:
                     k = 'Location'
                     v = '/'
                     returnStatement = """<p>Invalid login.  Please try again.</p>"""
           
                 else:
                     meeplib.set_curr_user(username)
                     k = 'Location'
                     v = '/main_page'
             else:      
                 returnStatement = """password none"""
        else:
            returnStatement = """username none"""

        # set content-type
        headers = [('Content-type', 'text/html')]
       
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return """Invalid Password. Please try again."""     

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
            s.append("<form action='delete_action' method='POST'><input type='number' hidden='true' name='mid' value=%d><input type='submit' value='Delete'></form>" % (m.id))
            s.append('<hr>')

        s.append("<a href='../main_page'>Back</a>")
            
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
    
        username = meeplib.get_curr_user()
        user =  meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/messages'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""


    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        messageId = form['mid'].value
        message = meeplib.get_message(int(messageId))
        meeplib.delete_message(message)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/messages'))
        start_response("302 Found", headers)
        return ["message deleted"]
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/main_page': self.main_page,
                      '/create_user': self.create_user,
                      '/create_user_action':self.create_user_action,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/messages': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete': self.delete_message,
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
