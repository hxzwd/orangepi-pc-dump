#!/usr/bin/env python
# -*- coding: utf-8 -*-


from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler


host = ""
port = 8000

server_address = ( host, port )

httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()

