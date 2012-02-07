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
        assert 'Add a topic' in data[0]
        assert 'Show topics' in data[0]
        
    def test_view_topic(self):
        environ = {}
        environ['PATH_INFO'] = '/m/topics/view'
        environ['QUERY_STRING'] = 'id=0'
        
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert 'First Topic' in data[0]
        
    def test_list_topics(self):
        environ = {}
        environ['PATH_INFO'] = '/m/list_topics'
        
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert 'First Topic' in data[0]
        
    def test_add_topic(self):
        environ = {}
        environ['PATH_INFO'] = '/m/add_topic'
        
        def fake_start_response(status, headers):
            assert status == '200 OK'
            assert ('Content-type', 'text/html') in headers
            
        data = self.app(environ, fake_start_response)
        assert 'Add a new topic' in data

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
