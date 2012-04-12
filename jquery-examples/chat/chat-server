import sys
from webserve import Server

port = sys.argv[1]
port = int(port)

from apps import ChatApp
chat_app = ChatApp('./html')

Server(port, chat_app).serve_forever()
