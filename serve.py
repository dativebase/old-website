#!/usr/bin/env python

"""Serves the www.onlinelinguisticdatabase.org web site locally. Usage:

    $ python serve.py

Or just:

    $ ./serve.py

Warning: SimpleHTTPServer is known to be slow. Using NodeJS's http-server or
twisted-py might be better, see
http://stackoverflow.com/questions/12905426/what-is-a-faster-alternative-to-pythons-simplehttpserver

"""

import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

# HandlerClass = SimpleHTTPRequestHandler

class HandlerClass(SimpleHTTPRequestHandler):
    """This is a single-page JavaScript-based web site. The server must route
    requests like /api to / and the JavaScript will handle the correct page
    display.

    """
    def do_GET(self):
        if self.path in ['/apps', '/faq', '/doc', '/api']:
            self.path = '/'
        return SimpleHTTPRequestHandler.do_GET(self)

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()

