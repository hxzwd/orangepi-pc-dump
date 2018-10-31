#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import time
import io

class Wall:
	USERS = "cgi-bin/users.json"
	WALL = "cgi-bin/wall.json"
	COOKIES = "cgi-bin/cookies.json"

	def __init__(self):
		try:
			with io.open(self.USERS, "r", encoding = "utf-8"):
				pass
		except Exception as excp:
			with io.open(self.USERS, "w", encoding = "utf-8") as f:
				json.dump({}, f)
		try:
			with io.open(self.WALL, "r", encoding = "utf-8"):
				pass
		except Exception as excp:
			with io.open(self.WALL, "w", encoding = "utf-8") as f:
				json.dump({ "posts" : [] }, f)
		try:
			with io.open(self.COOKIES, "r", encoding = "utf-8"):
				pass
		except Exception as excp:
			with io.open(self.COOKIES, "w", encoding = "utf-8") as f:
				json.dump({}, f)

	def find(self, user, password = None):
		with io.open(self.USERS, "r", encoding = "utf-8") as f:
			users = json.load(f)
		if user in users and (password is None or password == users[user]):
			return True
		return False

	def register(self, user, password):
		if self.find(user):
			return False
		with io.open(self.USERS, "r", encoding = "utf-8") as f:
			users = json.load(f)
		users[user] = password
		with io.open(self.USERS, "w", encoding = "utf-8") as f:
			json.dump(users, f)
		return True

	def set_cookie(self, user):
		with io.open(self.COOKIES, "r", encoding = "utf-8") as f:
			cookies = json.load(f)
		cookie = str(time.time()) + str(random.randrange(10**14))
		cookies[cookie] = user
		with io.open(self.COOKIES, "w", encoding = "utf-8") as f:
			json.dump(cookies, f)
		return cookie

	def find_cookie(self, cookie):
		with io.open(self.COOKIES, "r", encoding = "utf-8") as f:
			cookies = json.load(f)
		return cookies.get(cookie)

	def publich(self, user, text):
		with io.open(self.WALL, "r", encoding = "utf-8") as f:
			wall = json.load(f)
		wall["posts"].append({ "user" : user, "text" : text })
		with io.open(self.WALL, "w", encoding = "utf-8") as f:
			json.dump(wall, f)

	def html_list(self):
		with io.open(self.WALL, "r", encoding = "utf-8") as f:
			wall = json.load(f)
		posts = []
		for post in wall["posts"]:
			content = post["user"] + " : " + post["text"]
			posts.append(content)
		return "<br>".join(posts)

