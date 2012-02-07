import unittest
import meep_example_app
import meeplib
class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app

    def test_index(self):
        environ = {} # make a fake dict
        environ['PATH_INFO'] = '/'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        assert 'Add a message' in data[0]
        assert 'Show messages' in data[0]

    def test_list_messages(self):
        environ = {} # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)

        assert 'id:' in data[0]
        assert 'title:' in data[0]
        assert 'author:' in data[0]
        assert 'message:' in data[0]
        assert 'Reply' in data[0]
        assert 'Delete Message' in data[0]
        assert 'Search' in data[0]
        
    def test_delete(self):
        u = meeplib.User('foo', 'bar')
        m = meeplib.Message('my title', 'This is my message!', u)

        assert m in meeplib._messages.values()

        meeplib.delete_message(m)

        assert m not in meeplib._messages.values()


    def test_add(self):
        u = meeplib.User('bar', 'foo')
        m = meeplib.Message('The Title', 'Content', u)

        assert m in meeplib._messages.values()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
