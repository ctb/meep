import sys
from webserve import Server

port = sys.argv[1]
port = int(port)

from apps import QuotesApp
quotes_app = QuotesApp('quotes.txt', './html')

Server(port, quotes_app).serve_forever()
