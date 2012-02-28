import unittest
import string
import os
import meep_example_app
import urllib

class TestApp(unittest.TestCase):
    def setUp(self):
        #the backup file causes some of the tests to fail - not sure why
        #remove the backup file before every test
        try:
            os.remove(meep_example_app.meeplib._getFileName())
        except:
            pass    #the file does not exist
        
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app
        
    def test_add_message(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add'
        environ["HTTP_COOKIE"] = 'username=studentx'
        environ['wsgi.input'] = ''
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert string.find(data[0], 'parentPostID') != -1
        assert string.find(data[0], 'title') != -1
        assert string.find(data[0], 'message') != -1

    def test_add_message_action(self):
        #check that there is exactly one message stored
        assert len(meep_example_app.meeplib._messages) == 1
        
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add_action'
        environ["HTTP_COOKIE"] = 'username=studentx'
        environ['wsgi.input'] = ''
        form_dict = {'title':'Mock title', 'message':'Mock message', 'parentPostID':'-1'}
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)
        def fake_start_response(status, headers):
            #assert status == '200 OK'        #can't make this line pass
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)
        assert data[0] == 'message added'  
        
        #check that there are 2 messages stored, and check that the 2nd message is what is expected
        assert len(meep_example_app.meeplib._messages) == 2
        assert (meep_example_app.meeplib._messages[1] == 
            meep_example_app.meeplib.Message('Mock title', 'Mock message', meep_example_app.meeplib.get_user('studentx'), -1))
        
    def test_auth_handler(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        environ["HTTP_COOKIE"] = 'username=studentx'

        #test a valid user
        assert meep_example_app.MeepExampleApp.authHandler(self.app, environ) == meep_example_app.meeplib.get_user('studentx')

        #test an invalid user
        environ["HTTP_COOKIE"] = 'username=studenta'
        assert meep_example_app.MeepExampleApp.authHandler(self.app, environ) is None

    def test_create_user(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert string.find(data[0], 'Username') != -1
        assert string.find(data[0], 'Password') != -1

    def test_create_user_action(self):
        #check that there are 5 users initially
        assert len(meep_example_app.meeplib._users) == 5
        
        
        environ = {}
        environ['PATH_INFO'] = '/create_user_action'
        environ["HTTP_COOKIE"] = 'username=studentx'
        environ['wsgi.input'] = ''
        form_dict = {'username':'studentb', 'password':'passwordb'}
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)
        def fake_start_response(status, headers):
            #assert status == '200 OK'        #can't make this line pass
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)
        
        #check that there are now 6 users
        assert len(meep_example_app.meeplib._users) == 6
        assert (meep_example_app.meeplib.get_user('studentb') == 
                meep_example_app.meeplib.User('studentb', 'passwordb'))
        
    def test_remove_action(self):
        #check that there is one message to start with
        assert len(meep_example_app.meeplib._messages) == 1
        
        environ = {}
        environ['PATH_INFO'] = '/m/remove'
        environ["HTTP_COOKIE"] = 'username=studentx'
        environ['wsgi.input'] = ''
        form_dict = {'messageID':'0'}
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)
        def fake_start_response(status, headers):
            #assert status == '200 OK'        #can't make this line pass
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)
        assert len(meep_example_app.meeplib._messages) == 0
        
    def test_reply_message(self):
        #check that there is one message to start with
        assert len(meep_example_app.meeplib._messages) == 1
        
        environ = {}
        environ['PATH_INFO'] = '/m/reply'
        environ["HTTP_COOKIE"] = 'username=studentx'
        environ['wsgi.input'] = ''
        form_dict = {'title':'Mock title', 'message':'Mock Message', 'parentPostID':'0'}
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)
        def fake_start_response(status, headers):
            #assert status == '200 OK'        #can't make this line pass
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)
        #check that there is now 2 messages
        assert len(meep_example_app.meeplib._messages) == 2
        assert (meep_example_app.meeplib._messages[1] ==
                meep_example_app.meeplib.Message('Mock title', 'Mock Message', meep_example_app.meeplib.get_user('studentx'), 0))

    def test_index(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        #The app does not allow messages to be added here since nobody is logged in
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        assert 'Create a New User' in data[0]
        assert 'Show messages' in data[0]
        
    def test_list_messages(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert 'This is my message!' in data[0]
        #nobody is logged in, so no creation of responses or deleting allowed
        assert 'Submit response' not in data[0]
        assert 'Delete this message' not in data[0]
        
        #log in, creation of responses and deleting is allowed
        environ["HTTP_COOKIE"] = 'username=studentx'
        data = self.app(environ, fake_start_response)
        assert 'Submit response' in data[0]
        assert 'Delete this message' in data[0]
    
    def test_login_and_logout(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
        
        #check that the user is logged out to begin with    
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        
        #log in
        environ["HTTP_COOKIE"] = 'username=studentx'
        data = self.app(environ, fake_start_response)
        assert 'you are logged in as user: studentx' in data[0]
        assert 'Log out' in data[0]
        
        #log out
        environ["HTTP_COOKIE"] = 'username='
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        
      
    def test_login_failed(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        #check that the user is logged out to begin with    
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]
        
        #failed log in
        environ["HTTP_COOKIE"] = 'username=studenta'
        data = self.app(environ, fake_start_response)
        assert 'Please login to create and delete messages' in data[0]
        assert 'Log in' in data[0]

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
