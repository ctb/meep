import unittest
import meep_example_app

class TestApp(unittest.TestCase):
    def setUp(self):
        app = meep_example_app.MeepExampleApp()
        self.app = app

    def test_index(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Show messages' in data[0]
        assert 'Create a New User' in data[0]

    def test_show_messages(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'my title' in data[0]
        assert 'This is my message!' in data[0]
        

    def test_delete_message_action(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'delete message 0' in data[0]

    def test_reply_message_action(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Reply' in data[0]

    def test_CreateUser(self):
       environ = {}
       environ['PATH_INFO'] ='/create_user'
       environ['wsgi.input'] = ''
       def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

       data = self.app(environ, fake_start_response)
       assert 'username:' in data[0]
       assert 'password:' in data[0]
       assert 'confirm password:' in data[0]

    def test_Login(self):
       environ = {}
       environ['PATH_INFO'] ='/login'
       environ['wsgi.input'] = ''
       def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

       data = self.app(environ, fake_start_response)
       assert 'Or Create a New User' in data[0]
       assert 'username' in data[0]
       assert 'password' in data[0]
      

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

