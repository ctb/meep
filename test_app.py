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
        assert 'Create a New User' in data[0]
        assert 'Show messages' in data[0]

    def test_CreateUser(self):
       environ = {}
       environ['PATH_INFO'] ='/create_user'
       environ['wsgi.input'] = ''
       def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

       data = self.app(environ, fake_start_response)

    def test_Login(self):
       environ = {}
       environ['PATH_INFO'] ='/login'
       environ['wsgi.input'] = ''
       def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

       data = self.app(environ, fake_start_response)

    def test_Show_Messages(self):
       environ = {}
       environ['PATH_INFO'] ='/m/list'
       environ['wsgi.input'] = ''
       def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

       data = self.app(environ, fake_start_response)
        

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()