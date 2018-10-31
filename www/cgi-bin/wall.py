#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import html
import Cookie as cookies
import os

from _wall import Wall

wall = Wall()

cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")

if session is not None:
	session = session.value

user = wall.find_cookie(session)

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if action == "publish":
	text = form.getfirst("text", "")
	text = cgi.escape(text)
	if text and user is not None:
		wall.publish(user, txt)
elif action == "login":
	login = cgi.escape(form.getfirst("login", ""))
	password = cgi.escape(form.getfirst("password", ""))
	if wall.find(login, password):
		cookie = wall.set_cookie(login)
		print "Set-cookie: session={0}".format(cookie)
	elif wall.find(login):
		pass
	else:
		wall.register(login, password)
		cookie = wall.set_cookie(login)
		print "Set-cookie: session={0}".format(cookie)


pattern = """ <!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Wall page</title>
</head>
<body>
	Form of loggining and registration. Unknown login will be registered
	<form action="/cgi-bin/wall.py">
		Login: <input type = "text" name = "login">
		Password: <input type = "text" name = "password">
		<input type = "hidden" name = "action" value = "login">
		<input type = "submit">
	</form>

	{posts}

	{publish}
</body>
</html>
"""


if user is not None:
	pub = """<form action = "/cgi-bin/wall.py">
		<textarea name = "text"></textarea>
		<input type = "hidden" name = "action" value = "publish">
		<input type = "submit">
	</form>
"""
else:
	pub = ""

print "Content-type: text/html\n"
print pattern.format(posts = wall.html_list(), publish = pub)

