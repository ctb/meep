from meep_example_app import MeepExampleApp
from wsgiref.simple_server import make_server

app = MeepExampleApp()

httpd = make_server('', 8000, app)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()

# Alternative: serve one request, then exit
httpd.handle_request()
