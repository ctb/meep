import meeplib
import traceback
import cgi

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a thread
    t = meeplib.Thread()
    # create a single message
    m = meeplib.Message('This is my message!', u,'Test Thread')
    # save the message in the thread
    t.add_post(m)

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

        return ["""you are logged in as user: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]

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
        threads = meeplib.get_all_threads()

        s = []
        if threads:
            for t in threads:
                for m in t.get_all_posts():
                    s.append('<hr>')
                    if m.title != "": 
                        s.append('<h2>%s</h2>' % (m.title))
                    s.append('<p>%s</p>' % (m.post))
                    s.append('<p>Posted by: %s</p>' % (m.author.username))
                    # append the delete message link
                    s.append("""
                    <form action='delete_action' method='POST'><input name='id' type='hidden' value='%d' /><input type='submit' value='Delete Message' /></form>
                    """  % (m.id))
                s.append("""
                <form action='reply' method='POST'><input name='thread_id' type='hidden' value='%d' /><input type='submit' value='Reply to' /></form>
                """ % (t.id))
        else:
            s.append("There are no messages to display.<p>")

        s.append('<hr>')
        s.append("<a href='../../'>index</a>")
            
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
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id = int(form['id'].value)

        msg = meeplib.get_message(id)
        meeplib.delete_message(msg)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        return["message deleted"]
        
    def reply(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        thread_id = int(form['thread_id'].value)
        t = meeplib.get_thread(thread_id)
        
        s = []
        for m in t.get_all_posts():
            s.append('<hr>')
            if m.title != "": 
                s.append('<h2>%s</h2>' % (m.title))
            s.append('<p>%s</p>' % (m.post))
            s.append('<p>Posted by: %s</p>' % (m.author.username))
        s.append('<hr>')
        s.append("""
        <form action='reply_action' method='POST'>
        <input name='thread_id' type='hidden' value='%d' />
        Message:<input type='text' name='post'><br>
        <input type='submit'>
        </form>
        """ % (t.id))
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        return ["".join(s)]

    def reply_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        post = form['post'].value

        username = 'test'
        user = meeplib.get_user(username)

        new_message = meeplib.Message(post, user)
        thread_id = int(form['thread_id'].value)
        
        t = meeplib.get_thread(thread_id)
        t.add_post(new_message)
        

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["reply added"]

    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete_action': self.delete_message_action,
                      '/m/reply': self.reply,
                      '/m/reply_action': self.reply_action
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
