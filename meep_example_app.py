import meeplib
import traceback
import cgi
import meepcookie

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message and topic
    meeplib.Topic('First Topic', meeplib.Message('my title', 'This is my message!', u), u)
    
    meeplib.load_data()

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

        #return ["""You are logged in as: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]
        return ["""You are logged in as: %s.<p><a href='/m/add_topic'>Add a topic</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list_topics'>Show topics</a>""" % (username,)]

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

    def list_topics(self, environ, start_response):
        topics = meeplib.get_all_topics()
        
        s = []
        for t in topics:
            s.append("<a href='/m/topics/view?id=%d'>%s</a>" % (int(t.id), t.title))
            s.append('<hr>')
            
        s.append("<a href='../../'>index</a>")
        
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
            s.append("""
            <form name='delete_%d' action='../delete_message_topic' method='POST'>
                <input type='hidden' name='id' value='%d' />
                <input type='hidden' name='topic_id' value='%s' />
                <input type='submit' value='Delete Message' />
            </form>""" % (m.id,m.id,tId,))
            s.append("""
            <form name='reply_%d' action='../reply_topic' method='POST'>
                <input type='hidden' name='id' value='%d' />
                <input type='hidden' name='topic_id' value='%s' />
                <input type='submit' value='Reply to Message' />
            </form>""" % (m.id,m.id,tId,))
            s.append('<hr>')

        s.append("<form action='../add_message_topic_action' name='add_message' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='number' hidden='true' name='topicid' value=%d><input type='submit'></form>" % (topic.id))
        
        s.append("<br><form action='../delete_topic_action' name='delete_topic' method='POST'><input type='number' hidden='true' name='tid' value=%d><input type='submit' value='Delete topic'></form>" % (topic.id))
        
        s.append("<a href='../../'>index</a>")
            
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
            s.append("""
            <form action='delete_message' method='POST'>
                <input type='hidden' name='id' value='%d' />
                <input type='submit' value='Delete Message' />
            </form>""" % (m.id,))
            s.append("""
            <form action='reply' method='POST'>
                <input type='hidden' name='id' value='%d' />
                <input type='submit' value='Reply to Message' />
            </form>""" % (m.id,))
            s.append('<hr>')

        s.append("<a href='../../'>index</a>")
            
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
        
        meeplib.save_data()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic added"]
        
    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""

    def add_message_action(self, environ, start_response):
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)
        
        meeplib.save_data()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]
        
    def delete_message(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        id = int(form['id'].value)
        
        message = meeplib.get_message(id)
        
        meeplib.delete_message(message)
        
        meeplib.save_data()
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message deleted"]
        
    def delete_message_topic(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        topic_id = int(form['topic_id'].value)
        id = int(form['id'].value)
        
        message = meeplib.get_message(id)
        topic = meeplib.get_topic(topic_id)
        
        topic.delete_message_from_topic(message)
        
        meeplib.save_data()
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/topics/view?id=%d' % (topic_id,)))
        start_response("302 Found", headers)
        return ["message deleted"]
        
    def reply(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        id = int(form['id'].value)
        
        m = meeplib.get_message(id)
        
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """
        <form action='add_action' method='POST'>
            Title: <input type='text' name='title' value='RE: %s'><br>
            Message:<input type='text' name='message' value='<br>In post %d, %s said:<blockquote>%s</blockquote>'><br>
            <input type='submit'>
        </form>""" % (m.title, m.id, m.author.username, m.post)
        
    def reply_topic(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        
        id = int(form['id'].value)
        topic_id = int(form['topic_id'].value)
        
        m = meeplib.get_message(id)
        
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """
        <form action='add_message_topic_action' method='POST'>
            Title: <input type='text' name='title' value='RE: %s'><br>
            Message:<input type='text' name='message' value='<br>In post %d, %s said:<blockquote>%s</blockquote>'><br>
            <input type='hidden' name='topicid' value='%d'>
            <input type='submit'>
        </form>""" % (m.title, m.id, m.author.username, m.post, topic_id)
		
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
        
        meeplib.save_data()
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/topics/view?id=%d' % (topic.id)))
        start_response("302 Found", headers)
        return ["message added to topic"]
        
    def delete_topic_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        topicId = form['tid'].value
        topic = meeplib.get_topic(int(topicId))
        meeplib.delete_topic(topic)
        
        meeplib.save_data()
        
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list_topics'))
        start_response("302 Found", headers)
        return ["topic deleted"]

    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/list_topics': self.list_topics,
                      '/m/topics/view': self.view_topic,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete_message': self.delete_message,
                      '/m/delete_message_topic': self.delete_message_topic,
                      '/m/reply': self.reply,
                      '/m/reply_topic': self.reply_topic,
                      '/m/add_message_topic_action': self.add_message_topic_action,
                      '/m/add_topic': self.add_topic,
                      '/m/add_topic_action': self.add_topic_action,
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
