import unittest
import urllib
import sys
import os.path
cwd = os.path.dirname(__file__)
importdir = os.path.abspath(os.path.join(cwd, '../'))
if importdir not in sys.path:
    sys.path.append(importdir)
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
        assert 'Log in' in data
        assert 'Create a New User' in data

    def test_index_with_auth(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        environ['HTTP_COOKIE'] = "username=test"

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'New thread' in data
        assert 'Show threads' in data

    def test_thread_list(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'index' in data[0]

    def test_create_user(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'username:' in data[0]
        assert 'password:' in data[0]
        assert 'confirm password:' in data[0]

    def test_create_user_action(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/create_user'
        environ['wsgi.input'] = ''

        form_dict = {}
        form_dict['username'] = "apptest"
        form_dict['password'] = "pass"
        form_dict['password_confirm'] = "pass"
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)

        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/'
        environ['wsgi.input'] = ''
        environ['HTTP_COOKIE'] = "username=apptest"

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        assert "apptest" in data[0]

    def test_create_thread(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add_thread'
        environ['wsgi.input'] = ''
        environ['HTTP_COOKIE'] = "username=test"

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Title:' in data[0]
        assert 'Message:' in data[0]

    def test_create_thread_action(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add_thread'
        environ['wsgi.input'] = ''
        environ['HTTP_COOKIE'] = "username=test"

        form_dict = {}
        form_dict['title'] = "Test title"
        form_dict['message'] = "Test message"
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)

        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)

        assert 'index' in data[0]
        assert "Test title" in data[0]
        assert "Test message" in data[0]

    def test_reply(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/reply'
        environ['wsgi.input'] = ''
        environ['HTTP_COOKIE'] = "username=test"

        form_dict = {}
        form_dict['thread_id'] = 0
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert "Message:" in data[0]

    def test_reply_action(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/reply'
        environ['wsgi.input'] = ''
        environ['HTTP_COOKIE'] = "username=test"

        form_dict = {}
        form_dict['thread_id'] = 0
        form_dict['post'] = "replytest"
        environ['QUERY_STRING'] = urllib.urlencode(form_dict)

        def fake_start_response(status, headers):
            assert status == '302 Found'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)

        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)

        assert 'index' in data[0]
        assert "replytest" in data[0]

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
