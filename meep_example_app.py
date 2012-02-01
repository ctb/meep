import meeplib
import traceback
import cgi

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a thread
    t = meeplib.Thread('Test Thread')
    # create a single message
    m = meeplib.Message('This is my message!', u)
    # save the message in the thread
    t.add_post(m)

    # done.

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def __init__(self):
        self.username = None
        meeplib._threads, meeplib._user_ids, meeplib._users = meeplib.load_state()

    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        s=["""Please login to create and delete messages.<p><a href='/login'>Log in</a><p><a href='/create_user'>Create a New User</a><p>"""]
        if self.username is not None:
            s = ["""you are logged in as user: %s.<p><a href='/logout'>Log out</a><p><a href='/m/add_thread'>New thread</a><p><a href='/m/list'>Show threads</a>""" % (self.username,)]
        return s

    def login(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        try:
            username = form['username'].value
            # retrieve user
            #print "we gots a username", username
        except KeyError:
            username = ''
            #print "no user input"

        try:
            password = form['password'].value
            #print "we gots a password", password
        except KeyError:
            password = ''
            #print 'no password input'

        s=[]

        ##if we have username and password
        if username != '' and password != '':
            user = meeplib.get_user(username)
            if user is not None and user.password == password:
                ## send back a redirect to '/'
                k = 'Location'
                v = '/'
                headers.append((k, v))
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
        if self.username is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]
        self.username =  None

        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        return "no such content"

    def create_user(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        #print "form", form

        try:
            username = form['username'].value
            # retrieve user
            #print "we gots a username", username
        except KeyError:
            username = ''
            #print "no user input"

        try:
            password = form['password'].value
            #print "we gots a password", password
        except KeyError:
            password = ''
            #print 'no password input'

        try:
            password2 = form['password_confirm'].value
            #print "we gots a password", password
        except KeyError:
            password2 = ''
            #print 'no password confirmation'

        s=[]

        ##if we have username and password and confirmation password
        if username != '':
            user = meeplib.get_user(username)
            ## user already exists
            if user is not None:
                s.append('''Creation Failed! <br>
                    User already exists, please use a different username.<p>''')
            ## user doesn't exist but they messed up the passwords
            elif password == '':
                s.append('''Creation Failed! <br>
                    Please fill in the Password field<p>''')
            elif password != password2:
                s.append('''Creation Failed! <br>
                    The passwords you provided did not match.<p>''')
            else:
                u = meeplib.User(username, password)
                meeplib.save_state()
                ## send back a redirect to '/'
                k = 'Location'
                v = '/'
                headers.append((k, v))
                self.username = username
        elif password != '' or password2 != '':
            s.append('''Creation Failed! <br>
            Please provide a username<.p>''')


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
        threads = meeplib.get_all_threads()
        user = meeplib.get_user(self.username)
        s = []
        if threads:
            for t in threads:
                flag = 0
                for m in t.get_all_posts():
                    s.append('<hr>')
                    if flag == 0: 
                        s.append('<h2>%s</h2>' % (t.title))
                        flag = 1
                    s.append('<p>%s</p>' % (m.post))
                    s.append('<p>Posted by: %s</p>' % (m.author.username))
                    # append the delete message link
                    # only if currently logged in user owns that post
                    if m.author == user:
                        s.append("""
                        <form action='delete_action' method='POST'>
                        <input name='thread_id' type='hidden' value='%d' />
                        <input name='post_id' type='hidden' value='%d' />
                        <input type='submit' value='Delete Message' />
                        </form>
                        """  % (t.id, m.id))
                s.append("""
                <form action='reply' method='POST'>
                <input name='thread_id' type='hidden' value='%d' />
                <input type='submit' value='Reply to' />
                </form>
                """ % (t.id))
        else:
            s.append("There are no threads to display.<p>")

        s.append('<hr>')
        s.append("<a href='../../'>index</a>")
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return ["".join(s)]

    def add_thread(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        if self.username is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        try:
            title = form['title'].value
        except KeyError:
            title = ''
        try:
            message = form ['message'].value
        except KeyError:
            message = ''

        s = []

        # title and message are non-empty
        if title == '' and message == '':
            pass
        elif title == '' and message != '':
            s.append("Title was empty.<p>")
        elif title != '' and message == '':
            s.append("Message was empty. <p>")
        elif title != '' and message != '':
            user = meeplib.get_user(self.username)
            new_message = meeplib.Message(message, user)
            t = meeplib.Thread(title)
            t.add_post(new_message)
            meeplib.save_state()
            headers.append(('Location','/m/list'))
            
        start_response("302 Found", headers)

        # doesn't get executed if we had valid input and created a thread
        s.append("""
        <form action='add_thread' method='POST'>
        Title: <input type='text' name='title' value='%s'><br>
        Message: <input type='text' name='message' value='%s'><br>
        <input type='submit'></form>
        """ % (title, message))

        return ["".join(s)]

    def delete_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if self.username is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        thread_id = int(form['thread_id'].value)
        post_id = int(form['post_id'].value)

        t = meeplib.get_thread(thread_id)
        post = t.get_post(post_id)
        t.delete_post(post)
        meeplib.save_state()

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)

        return["post deleted"]
        
    def reply(self, environ, start_response):
        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        if self.username is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        thread_id = int(form['thread_id'].value)
        t = meeplib.get_thread(thread_id)
        
        s = []
        flag = 0
        for m in t.get_all_posts():
            s.append('<hr>')
            if flag == 0: 
                s.append('<h2>%s</h2>' % (t.title))
                flag = 1
            s.append('<p>%s</p>' % (m.post))
            s.append('<p>Posted by: %s</p>' % (m.author.username))
        s.append('<hr>')

        try:
            post = form['post'].value
        except KeyError:
            post = ''

        # post is non-empty
        if post != '':
            user = meeplib.get_user(self.username)
            new_message = meeplib.Message(post, user)
            t.add_post(new_message)
            meeplib.save_state()
            headers.append(('Location','/m/list'))

        start_response("302 Found", headers)

        # doesn't get executed unless we had valid input and replied to the thread
        s.append("""
        <form action='reply' method='POST'>
        <input name='thread_id' type='hidden' value='%d' />
        Message: <input type='text' name='post'><br>
        <input type='submit'>
        </form>
        """ % (t.id))

        return ["".join(s)]

    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/create_user': self.create_user,
                      '/m/list': self.list_messages,
                      '/m/add_thread': self.add_thread,
                      '/m/delete_action': self.delete_message_action,
                      '/m/reply': self.reply
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
