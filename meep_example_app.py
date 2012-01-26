import meeplib
import traceback
import cgi

def initialize():
    # create a default user with username: test, password: test
    u = meeplib.User('test', 'test')

    # create a single message and topic
    meeplib.Topic('First Topic', meeplib.Message('my title', 'This is my message!', u), u)

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'Not Logged in'

        #return ["""You are logged in as: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]
        #return ["""You are logged in as: %s.<p><a href='/m/add_topic'>Add a topic</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list_topics'>Show topics</a>""" % (username,)]
        return ["""
            Login or <a href='/create_user'>Create an Account</a>
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

        return ["""You have successfully logged in as: %s<p><a href='/m/add_topic'>Add a topic</a><p><p><a href='/m/list_topics'>Show topics</a><p><a href='/logout'>Log out</a>""" % (username,)]

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("302 Found", headers)
        return """
            Enter your username and password: <p><form action='create_user_action' method='POST'>
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

    def list_topics(self, environ, start_response):
        topics = meeplib.get_all_topics()
        
        s = []
        for t in topics:
            s.append("<a href='/m/topics/view?id=%d'>%s</a>" % (int(t.id), t.title))
            s.append('<hr>')
            
        s.append("<a href='../../main_page'>index</a>")
        
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]
        
    def view_topic(self, environ, start_response):
        qString = cgi.parse_qs(environ['QUERY_STRING'])
        tId = qString.get('id', [''])[0]
        topic = meeplib.get_topic(int(tId))
        messages = topic.get_messages()
        
        s = []
        s.append('%s<br><br>' % (topic.title))
        for m in messages:
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
            s.append("<form action='../delete_action' method='POST'><input type='number' hidden='true' name='mid' value=%d><input type='number' hidden='true' name='tid' value=%d><input type='submit' value='Delete message'></form>" % (m.id, topic.id))
            s.append('<hr>')

        s.append("<form action='../add_message_topic_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='number' hidden='true' name='topicid' value=%d><input type='submit'></form>" % (topic.id))
        
        s.append("<br><form action='../delete_topic_action' method='POST'><input type='number' hidden='true' name='tid' value=%d><input type='submit' value='Delete topic'></form>" % (topic.id))
        
        s.append("<a href='../../main_page'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]
    
    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()

        s = []
        for m in messages:
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
            s.append("<form action='delete_action' method='POST'><input type='number' hidden='true' name='mid' value=%d><input type='submit' value='Delete message'></form>" % (m.id))
            s.append('<hr>')

        s.append("<a href='../main_page'>Back</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

        
    def add_topic(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='add_topic_action' method='POST'>Add a new topic<br>Topic name: <input type='text' name='title'><br>Message title:<input type='text' name='msgtitle'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""
        
    def add_topic_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        msgtitle = form['msgtitle'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(msgtitle, message, user)
        new_topic = meeplib.Topic(title, new_message, user)
        

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic added"]
        
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
		
    def add_message_topic_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        topicId = form['topicid'].value
        topic = meeplib.get_topic(int(topicId))
        
        title = form['title'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)
        
        topic.add_message(new_message)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/topics/view?id=%d' % (topic.id)))
        start_response("302 Found", headers)
        return ["message added to topic"]
        
    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        messageId = form['mid'].value
        message = meeplib.get_message(int(messageId))
        meeplib.delete_message(message)
        #This could all be written on one line if one so chose
        #meeplib.delete_message(meeplib.get_message(int(form['mid'].value)))
        
        topicId = form['tid'].value
        topic = meeplib.get_topic(int(topicId))
        topic.delete_message_from_topic(message)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["message deleted"]
        
    def delete_topic_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        topicId = form['tid'].value
        topic = meeplib.get_topic(int(topicId))
        meeplib.delete_topic(topic)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic deleted"]

    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/main_page': self.main_page,
                      '/create_user': self.create_user,
                      '/create_user_action':self.create_user_action,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/list_topics': self.list_topics,
                      '/m/topics/view': self.view_topic,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/add_message_topic_action': self.add_message_topic_action,
                      '/m/add_topic': self.add_topic,
                      '/m/add_topic_action': self.add_topic_action,
					  '/m/delete_action': self.delete_message_action,
                      '/m/delete_topic_action': self.delete_topic_action
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
