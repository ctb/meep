#! /usr/bin/env python
import quixote.demo
from quixote.server.simple_server import run

run(quixote.demo.create_publisher, host='', port=8080)
