import unittest
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import meep_example_app

class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app

    def test_index(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Create an Account' in data[0]
        assert 'Username' in data[0]
        assert 'Password' in data[0]

    def test_main_page(self):
        environ = {}
        environ['PATH_INFO'] = '/main_page'
        
        #No user logged in, so we return 401 Unauthorized
        def fake_start_response(status, headers):
            assert status == '401 Unauthorized'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Click to login' in data[0]

        #Setup so that a user is logged in
        self.login_user()
        
        #User is logged in, return 200 OK
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'You have successfully logged in as: test' in data[0]
        assert 'Add a topic' in data[0]
        assert 'Show topics' in data[0]
        assert 'Log out' in data[0]
                
    def test_create_user(self):
        print "TestCreateUser"
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''
        def fake_start_response(status, headers):
            #print status
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Enter your username and password' in data[0]
        assert 'Username' in data[0]
        assert 'Password' in data[0]

    def test_create_user_action(self):
        pass

    def test_login(self):
        pass

    def test_logout(self):
        pass

    def test_list_topics(self):
        environ = {}
        environ['PATH_INFO'] = '/m/list_topics'
        
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'First Topic' in data[0]
        assert 'index' in data[0]

    def test_view_topic(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/topics/view'
        environ['QUERY_STRING'] = 'id=0'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'First Topic' in data[0]
        assert 'id: 0' in data[0]
        assert 'title: my title' in data[0]
        assert 'message: This is my message!' in data[0]
        assert 'author: test' in data[0]
        assert 'index' in data[0]

    def test_list_messages(self):
        pass

    def test_add_topic(self):
        pass

    def test_add_topic_action(self):
        pass

    def test_add_message(self):
        pass
    
    def test_add_message_action(self):
        pass
    
    def test_add_message_topic_action(self):
        pass    

    def test_delete_message_action(self):
        pass

    def test_delete_topic_action(self):
        pass

    def tearDown(self):
        pass

    def login_user(self):
        meep_example_app.meeplib.set_curr_user('test')
        
if __name__ == '__main__':
    unittest.main()
