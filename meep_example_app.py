import meeplib
import traceback
import cgi
import meepcookie
from Cookie import SimpleCookie, Morsel
from jinja2 import Environment, FileSystemLoader

def initialize():
    try:    
        meeplib._load_data()
    except IOError:  # file does not exist/cannot be opened
        # initialize data from scratch
        # create a default user with username: test, password: test
        u = meeplib.User('test', 'test')

        # create a single message and topic
        meeplib.Topic('First Topic', meeplib.Message('my title', 'This is my message!', u), u)

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
        #start_response("200 OK", [('Content-type', 'text/html')])
        username = ''
        # If a cookie exists, get it
        try:
            cookie_str = environ.get('HTTP_COOKIE', '')
            cookie = SimpleCookie(cookie_str)
            username = cookie["username"].value
            print "Login: Username = %s" % username
        except:
            print "session cookie not set! defaulting username"
            username = ''
        
        #If the cookie was found, redirect to main page, and set current user
        if username is not '':
            meeplib.set_curr_user(username)
            headers = [('Content-type', 'text/html')]
            headers.append(('Location','/main_page'))
            start_response("302 Found", headers)
            return "Cookie found, redirecting"
        #If the cookie wasn't found, prompt the user to login
        else:
            start_response("200 OK", [('Content-type', 'text/html')])
            return [ render_page('index.html') ]

    ###
    #   MAIN PAGE
    ###
    def main_page(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        try:
            meeplib.get_curr_user()
        except NameError:
            headers.append(('Location', '/'))
            start_response('401 Unauthorized', headers)
            return ["""<a href='/'>Click to login</a>"""]

        start_response("200 OK", headers)
        username = meeplib.get_curr_user()

        return [ render_page('main_page.html', username=username) ]

    ###
    #   CREATE USER
    ###
    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)
        return [ render_page('create_user.html') ]

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

    ###
    #   LOGIN
    ###
    def login(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        username = form['username'].value
        password = form['password'].value

        # set content-type
        headers = [('Content-type', 'text/html')]

        # Test whether variable is defined to be None
        if username is not None:
             if password is not None:
                 if meeplib.check_user(username, password) is False:
                     k = 'Location'
                     v = '/'
                     returnStatement = """Invalid login"""
           
                 else:
                     meeplib.set_curr_user(username)
                     k = 'Location'
                     v = '/main_page'
                     # Create and set the cookie
                     cookie_name, cookie_val = \
                                meepcookie.make_set_cookie_header('username', username)
                     headers.append((cookie_name, cookie_val))
             else:      
                 returnStatement = """password none"""
        else:
            returnStatement = """username none"""

        headers.append((k, v))
        start_response('302 Found', headers)
        
        return """Invalid Password. Please try again."""     

    ###
    #   LOGOUT
    ###
    def logout(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        #Clear the cookie
        try:
            cookie_str = environ.get('HTTP_COOKIE', '')
            cookie = SimpleCookie(cookie_str)
            #I was trying to be fancy here, but couldn't get it to work
            #cookie['username']['expires'] = meepcookie.cookie_expiration_date(-1)
            cookie_name, cookie_val = \
                                meepcookie.make_set_cookie_header('username', '')
            headers.append((cookie_name, cookie_val))
        except:
            print "No cookie exists (this probably shouldn't happen)"

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "Logged out"

    ###
    #   LIST TOPICS
    ###
    def list_topics(self, environ, start_response):
        topics = meeplib.get_all_topics()   
        
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return [ render_page('view_topics.html', topics = topics) ]        
        
    ###
    #   VIEW TOPIC
    ###
    def view_topic(self, environ, start_response):
        qString = cgi.parse_qs(environ['QUERY_STRING'])
        tId = qString.get('id', [''])[0]
        topic = meeplib.get_topic(int(tId))
        messages = topic.get_messages()
        
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return [ render_page('view_topic.html', messages=messages, topic=topic) ]
    
    ###
    #   VIEW MESSAGES
    ###
    """ 
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
    """
    
    ###
    #   ADD TOPIC
    ###
    def add_topic(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return [ render_page('add_topic.html') ]
        
    def add_topic_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #Get values off form
        title = form['title'].value
        msgtitle = form['msgtitle'].value
        message = form['message'].value
        
        #Get the current user
        username = meeplib.get_curr_user()
        user = meeplib.get_user(username)
        
        #Create new message and topic
        new_message = meeplib.Message(msgtitle, message, user)
        new_topic = meeplib.Topic(title, new_message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic added"]
        
    ###
    #   ADD MESSAGE
    ###
    """
    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""

    def add_message_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #Get values off the form
        title = form['title'].value
        message = form['message'].value
    
        #Get current user
        username = meeplib.get_curr_user()
        user =  meeplib.get_user(username)

        #Create new message
        new_message = meeplib.Message(title, message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/messages'))
        start_response("302 Found", headers)
        return ["message added"]
    """

    ###
    #   ADD MESSAGE TO TOPIC
    ###
    def add_message_topic_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #Get values off the form
        topicId = form['topicid'].value        
        title = form['title'].value
        message = form['message'].value
        
        #Get the topic and user
        topic = meeplib.get_topic(int(topicId))
        username = meeplib.get_curr_user()
        user = meeplib.get_user(username)
        
        #Add the message to the topic
        new_message = meeplib.Message(title, message, user)
        topic.add_message(new_message)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/topics/view?id=%d' % (topic.id)))
        start_response("302 Found", headers)
        return ["message added to topic"]
        
    ###
    #   DELETE MESSAGE
    ###
    def delete_message_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        #Get the message
        messageId = form['mid'].value
        message = meeplib.get_message(int(messageId))
        
        #Delete the message from the topic
        topicId = form['tid'].value
        topic = meeplib.get_topic(int(topicId))
        topic.delete_message_from_topic(message)
        
        #Delete the message altogether
        meeplib.delete_message(message)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["message deleted"]
        
    ###
    #   DELETE TOPIC
    ###
    def delete_topic_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        topicId = form['tid'].value
        topic = meeplib.get_topic(int(topicId))
        meeplib.delete_topic(topic)
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic deleted"]

    ###
    #   CALL HANDLER
    ###
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/main_page': self.main_page,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/create_user': self.create_user,
                      '/create_user_action':self.create_user_action,
                      #'/m/list': self.list_messages,
                      '/m/list_topics': self.list_topics,
                      '/m/topics/view': self.view_topic,
                      #'/m/add': self.add_message,
                      #'/m/add_action': self.add_message_action,
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