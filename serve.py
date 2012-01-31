from meep_example_app import MeepExampleApp, initialize
from wsgiref.simple_server import make_server

initialize()
app = MeepExampleApp()

httpd = make_server('', 8000, app)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()

# Alternative: serve one request, then exit
httpd.handle_request()

#updated 11/18/2011