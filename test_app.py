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
   
        assert 'Add a message' in data[0]
        assert 'Show messages' in data[0]


        
    def test_show_messages(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/list'

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)

        assert 'id: 0' in data[0]              ##key features are present
        assert 'Reply' in data[0]
        assert 'Delete' in data[0]
        assert 'Search' in data[0]

##    def test_search_messages(self):
##        environ = {}                    # make a fake dict
##        environ['PATH_INFO'] = '/m/search'
##
##        def fake_start_response(status, headers):
##            print "STATUS", status
##            assert status == '200 OK'
##            assert ('Content-type', 'text/html') in headers
##        data = self.app(environ, fake_start_response)
##
##        assert 'Your Search Results' in data[0]              ##key features are present
##        assert 'Reply' in data[0]
##        assert 'Delete' in data[0]
##        assert 'Search for Messages?' in data[0]
    def test_reply_box(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add_reply_action'
        environ['wsgi.input'] = """FieldStorage(None, None, [MiniFieldStorage('message_id', '0'), MiniFieldStorage('reply', 'COW')])"""

        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
        data = self.app(environ, fake_start_response)

        assert 'Reply' in data[0]              ##key features are present
    def test_add_message(self):
        environ = {}                    # make a fake dict
        environ['PATH_INFO'] = '/m/add'


        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers

        data = self.app(environ, fake_start_response)
        print "DATA", data
        assert 'Title:' in data              ##key features are present
        assert 'Message:' in data 
    def tearDown(self):
        pass

    
        

if __name__ == '__main__':
    unittest.main()
