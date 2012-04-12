import socket
from cStringIO import StringIO
import urlparse

class StartResponse(object):
    def __call__(self, status, headers):
        self.status = status
        self.headers = headers

class Server(object):
    def __init__(self, port, wsgi_app):
        self.port = port
        self.wsgi_app = wsgi_app

    def request_is_complete(self, data):
        """
        Evaluate data -- is this a complete (GET or POST) request?
        """
        if '\r\n\r\n' not in data:
            return False
        
        head, rest = data.split('\r\n\r\n', 1)
        request_line, head = head.split('\r\n', 1)
        reqtype, url, protocol = request_line.split(' ')

        parsed_url = urlparse.urlparse(url)
        path = parsed_url.path

        # process headers
        headers = head.splitlines()
        headers = [ x.split(': ', 1) for x in headers ]

        if reqtype != 'POST':
            contentsize = 0
        else:
            contentsize = None
            for k, v in headers:
                if k.lower() == 'content-length':
                    contentsize = int(v)

        if len(rest) == contentsize:
            return True

        return False

    def parse_request(self, data):
        if '\r\n\r\n' not in data:
            return False
        
        head, rest = data.split('\r\n\r\n', 1)
        request_line, head = head.split('\r\n', 1)
        request_type, url, protocol = request_line.split(' ')

        parsed_url = urlparse.urlparse(url)
        path = parsed_url.path
        query = parsed_url.query

        # process headers
        headers = head.splitlines()
        headers = [ x.split(': ', 1) for x in headers ]

        environ = {}
        environ['REQUEST_METHOD'] = request_type
        environ['SCRIPT_NAME'] = ''
        environ['PATH_INFO'] = path
        environ['SERVER_PROTOCOL'] = protocol
        environ['QUERY_STRING'] = query
        environ['wsgi.input'] = StringIO(rest)

        start_response = StartResponse()

        data = list(self.wsgi_app(environ, start_response))
        data = "".join(data)

        status = start_response.status
        headers = start_response.headers

        headers = "\r\n".join([ ": ".join(x) for x in headers ])

        return "HTTP/1.0 %s\r\n%s\r\n\r\n%s" % (status, headers, data)

    def handle_connection(self, sockobj, data_so_far=None):
        if data_so_far is None:    # initialize
            data_so_far = ''

        try:
            data = sockobj.recv(4096)
        except socket.error:
            return False, data_so_far

        data_so_far += data
        if self.request_is_complete(data_so_far): # complete request?
            response = self.parse_request(data_so_far)
            try:
                sockobj.sendall(response)
                sockobj.close()
            except socket.error:
                pass

            return True, None

        # not done yet; keep gathering information
        return False, data_so_far

    def serve_forever(self):
        print "binding '%s', port %d" % ('', self.port)
        sock = socket.socket()
        sock.bind( ('', self.port) )
        sock.listen(5)

        while 1:
            client_sock, client_addr = sock.accept()
            print '----'
            print 'connection:', client_addr

            close_flag, data = self.handle_connection(client_sock)
            while not close_flag:
                close_flag, data = self.handle_connection(client_sock, data)
            client_sock.close()

            print 'done with', client_addr
