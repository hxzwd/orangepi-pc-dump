#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Cookie as cookies

cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
name = cookie.get("name")

if name is None:
	print "Set-cookie: name=value; expires=Wed May 18 03:33:20 2033; path=/cgi-bin/; httponly"
	print "Content-type: text/html\n"
	print "Cookies test!!!"
else:
	print "Content-type: text/html\n"
	print "Cookies: {0}".format(name.value)



