#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import html



form = cgi.FieldStorage()

text1 = form.getfirst("text1", "Пустое")
text2 = form.getfirst("text2", "Пустое")

text1 = cgi.escape(text1)
text2 = cgi.escape(text2)

print "Content-type: text/html\n"
print """<!DOCTYPE HTML>
	<html>
	<head>
		<meta charset="utf-8">
		<title>Обработка данных формы</title>
	</head>
	<body>"""
print "<h1>Обработка данных формы</h1>"
print "<p>text1: {0}</p>".format(text1)
print "<p>text2: {0}</p>".format(text2)
print """</body>
	</html>"""

