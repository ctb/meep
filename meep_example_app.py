import meeplib
import meepcookie
import Cookie
import traceback
import cgi

from jinja2 import Environment, FileSystemLoader

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

env = Environment(loader=FileSystemLoader('templates'))

# render jinja2 template page and return as string in HTTP response
def render_page(filename, **variables):
    template = env.get_template(filename)
    x = template.render(**variables)
    return str(x)

class MeepExampleApp(object):
    """
    WSGI app object.
    """
    def __init__(self):
        meeplib.load_state()

    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        return render_page("index.html", user=user)

    def login(self, environ, start_response):
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is not None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged out to use that feature."]

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
                # set the cookie to the username string
                cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',user.username)
                headers.append((cookie_name, cookie_val))
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
        s.append(render_page("login.html", username=username))
        return [''.join(s)]

    def logout(self, environ, start_response):
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        cookie_name, cookie_val = meepcookie.make_set_cookie_header('username','')
        headers.append((cookie_name, cookie_val))
        start_response('302 Found', headers)
        return "no such content"

    def create_user(self, environ, start_response):
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is not None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged out to use that feature."]

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
                cookie_name, cookie_val = meepcookie.make_set_cookie_header('username',username)
                headers.append((cookie_name, cookie_val))
        elif password != '' or password2 != '':
            s.append('''Creation Failed! <br>
            Please provide a username.<p>''')


        start_response('302 Found', headers)

        ##if we have a valid username and password this is not executed
        s.append(render_page("create_user.html", username=username))
        return [''.join(s)]

    def list_messages(self, environ, start_response):
        threads = meeplib.get_all_threads()
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        s = []
        if threads:
            s.append(render_page("list_threads.html", threads=threads, user=user))
        else:
            s.append("There are no threads to display.<p>")

        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)

        return ["".join(s)]

    def add_thread(self, environ, start_response):
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        headers = [('Content-type', 'text/html')]

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
            new_message = meeplib.Message(message, user)
            t = meeplib.Thread(title)
            t.add_post(new_message)
            meeplib.save_state()
            headers.append(('Location','/m/list'))
            
        start_response("302 Found", headers)

        # doesn't get executed if we had valid input and created a thread
        s.append(render_page("add_thread.html", title=title, message=message))

        return ["".join(s)]

    def delete_message_action(self, environ, start_response):
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

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
        # get cookie if there is one
        try:
            cookie = Cookie.SimpleCookie(environ["HTTP_COOKIE"])
            username = cookie["username"].value
            #print "Username = %s" % username
        except:
            #print "session cookie not set! defaulting username"
            username = ''
        
        user = meeplib.get_user(username)
        if user is None:
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/'))
            start_response("302 Found", headers)
            return ["You must be logged in to use that feature."]

        headers = [('Content-type', 'text/html')]

        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

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
            new_message = meeplib.Message(post, user)
            t.add_post(new_message)
            meeplib.save_state()
            headers.append(('Location','/m/list'))

        start_response("302 Found", headers)

        # doesn't get executed unless we had valid input and replied to the thread
        s.append(render_page("reply.html", thread_id=t.id))
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
