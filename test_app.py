import unittest
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
        
    def test_create_account(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Enter your username and password' in data[0]
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
        
    def test_show_topics(self):
        environ = {}
        environ['PATH_INFO'] = '/m/list_topics'
        
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'First Topic' in data[0]
        assert 'index' in data[0]

    def tearDown(self):
        pass

    def login_user(self):
        meep_example_app.meeplib.set_curr_user('test')
        
if __name__ == '__main__':
    unittest.main()
