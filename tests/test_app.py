import unittest
import sys
sys.path.append("..")
import meep_example_app

class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app

    def test_index_no_auth(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Log in' in data[0]
        assert 'Create a New User' in data[0]

    def test_index_with_auth(self):
        self.app.username = 'test' # force login
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'New thread' in data[0]
        assert 'Show threads' in data[0]

    '''def test_create_user(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'

        def fake_start_response(status, headers):
            print status
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        print data
        assert 'New thread' in data[0]
        assert 'Show threads' in data[0]'''

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
