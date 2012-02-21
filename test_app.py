import unittest
import meep_example_app
import twill
import meeplib

class TestApp(unittest.TestCase):
    def setUp(self):
        meep_example_app.initialize()
        app = meep_example_app.MeepExampleApp()
        self.app = app
        u = meeplib.User('foo', 'bar',-1)
        v = meeplib.User('foo2', 'bar2',-1)
        m = meeplib.Message('my title', 'lol', u,-1)

##    def test_index(self):
##        environ = {}                    # make a fake dict
##        environ['PATH_INFO'] = '/'
##
##        def fake_start_response(status, headers):
##
##            assert status == '200 OK'
##
##            assert ('Content-type', 'text/html') in headers
##
##        data = self.app(environ, fake_start_response)
##   
##        assert 'Add a message' in data[0]
##        assert 'Show messages' in data[0]
##
##
##        
##    def test_show_messages(self):
##        environ = {}                    # make a fake dict
##        environ['PATH_INFO'] = '/m/list'
##
##        def fake_start_response(status, headers):
##            assert status == '200 OK'
##            assert ('Content-type', 'text/html') in headers
##        data = self.app(environ, fake_start_response)
##
##        assert 'id: 0' in data[0]              ##key features are present
##        assert 'Reply' in data[0]
##        assert 'Delete' in data[0]
##        assert 'Search' in data[0]
##
##    def test_search_messages(self):
##        environ = {}                    # make a fake dict
##        environ['PATH_INFO'] = '/m/search'
##        environ['wsgi.input'] = 'asdf'   #how to pass something in for here
##        def fake_start_response(status, headers):
##            print "STATUS", status
##            assert status == '200 OK'
##            assert ('Content-type', 'text/html') in headers
##        data = self.app(environ, fake_start_response)
##        print "DATA",data[0]
##        assert 'Your Search Results' in data[0]              ##key features are present
##
##        assert 'Delete' in data[0]
##        assert 'Search for Messages?' in data[0]
##    def test_post_reply(self):
##        environ = {}
##        environ['PATH_INFO'] = '/m/post_reply'
##        environ['QUERY_STRING'] = 'id=0'
##
##        def fake_start_response(status, headers):
##            assert status == '200 OK'
##            assert ('Content-type', 'text/html') in headers
##
##        data = self.app(environ, fake_start_response)
##        assert 'Reply' in data
##    def test_add_message(self):
##        environ = {}                    # make a fake dict
##        environ['PATH_INFO'] = '/m/add'
##
##
##        def fake_start_response(status, headers):
##            assert status == '200 OK'
##            assert ('Content-type', 'text/html') in headers
##
##        data = self.app(environ, fake_start_response)
##        print "DATA", data
##        assert 'Title:' in data              ##key features are present
##        assert 'Message:' in data
    def test_twill_delete(self):
        twill.execute_file("C:/Users/Paul/meep/test_delete_messages.twill", initial_url='http://localhost:8000')
    def test_twill_index(self):
        twill.execute_file("C:/Users/Paul/meep/test_index.twill.txt", initial_url='http://localhost:8000')
    def test_twill_reply(self):
        twill.execute_file("C:/Users/Paul/meep/test_reply_messages.twill", initial_url='http://localhost:8000')
    def test_show_messages(self):
        twill.execute_file("C:/Users/Paul/meep/test_show_messages.twill", initial_url='http://localhost:8000')
    def test_search_messages(self):
        twill.execute_file("C:/Users/Paul/meep/test_search_messages.twill", initial_url='http://localhost:8000')
        
    def tearDown(self):
        pass

    
        

if __name__ == '__main__':
    unittest.main()
    
