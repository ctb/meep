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
        messages = meeplib.get_all_messages()

        template = """
		<form action='alterMessage' method='POST'>
			<div class="messageCont">
				<div class="messageTitle">
					<p>%s</p>
					<input type='submit' id='bttnSubmit' name='bttnSubmit' value='Delete' onclick="return confirm('Are you sure you want to delete this message?');" />
				</div>
				<div class="message">%s</div>
				<div class="messageReply">
					By: %s
				</div>
				<div class="replies">
					{replies}
				</div>
				<div class="messageReply">
					&nbsp;<a href="#">Reply</a>
				</div>
				<div class="replyCont">
					Reply: <textarea type='text' name='replyText' class="replyInput" rows="2" ></textarea>
					<input type='submit' id='bttnSubmit' name='bttnSubmit' value='Reply' />
				</div>
			</div>
			<input type='hidden' name='id' value='%d' />
		</form>
		"""
		
        replyTemp = """
<div class="reply">
	<p>%s</p>
	<div class="messageReply">
		By: %s
	</div>
</div>
"""  
        s = []
        for m in messages:
             msg = template % (m.title, m.post, m.author.username, m.id)
             replies = m.get_replies()
             rs = []
             for r in replies:
                 print r.post
                 rs.append(replyTemp% (r.post, r.author.username))
             msg = msg.replace('{replies}',"".join(rs))
             s.append(msg)
        
        html = open('messageList.html', 'r').read().replace('{messageList}',"".join(s))
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return html

    def alter_message_action(self, environ, start_response):
        try:
        	form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
            #params = dict([part.split('=') for part in environ['QUERY_STRING'].split('&')])
            #msgId = int(params['id'])
        except:
            headers = [('Content-type', 'text/html')]
            start_response("200 OK", headers)
            return ["Error Processing provided ID"]

        id = int(form['id'].value)
        
        action = form['bttnSubmit'].value
        print action
        print id
        
        msg = meeplib.get_message(id)
        
        if msg == None:
            headers = [('Content-type', 'text/html')]
            start_response("200 OK", headers)
            return ["""Message id %d could not be found.""" % (msgId,)]
        elif action == "Delete":
            print('deleting')
            meeplib.delete_message(msg)
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/m/list'))
            start_response("302 Found", headers)
            return ["message removed"]
        elif action == "Reply":
            print('replying')
            title = ""
            print form['replyText'].value
            message = form['replyText'].value
            username = 'test'
            user = meeplib.get_user(username)
            new_message = meeplib.Message(title, message, user, True)
            msg.add_reply(new_message)
            headers = [('Content-type', 'text/html')]
            headers.append(('Location', '/m/list'))
            start_response("302 Found", headers)
            return ["message removed"]


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
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/alterMessage': self.alter_message_action
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
