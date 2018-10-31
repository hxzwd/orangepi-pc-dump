#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys


from bottle import Bottle, run


host = "localhost"
port = 5000
server = None

host = "192.168.0.105"
port = 8080

server = Bottle()


@server.route("/")
def r_root():
	return "<h1>Root page</h1>"


@server.route("/index")
def r_index():
	return "<h1>Index page</h1>"


run(server, host = host, port = port)

