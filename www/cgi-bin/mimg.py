#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import io
import cgi
import html
import Cookie as cookies
import string
from functools import reduce

idir = "//home//hjk//www//static//models"
hrefdir = "/static/models/"
Dirs = []
Files = []
Info = {}

class F:
	funcs = None
	def __init__(self, f):
		self.funcs = f
	def getf(self):
		def wrapper(x):
			z = x
			for i in self.funcs:
				z = apply(i, [z])
			return z
		return wrapper
	def getf2(self):
		def wrapper(x):
			z = x
			for i in self.funcs[:-1]:
				z = apply(i, [z])
			z = apply(self.funcs[-1], list(z))
			return z
		return wrapper

def FF(x):
	if len(x) == 1:
		return x
	else:
		return [ apply(x[0], FF(x[-1])) ]

FF_ = lambda z: reduce(lambda x, y: [y] + [x]*(type(x) is not int) + [[x]]*(type(x) is int), z)


#def FF_(x):
#	c = [x[0]]
#	for i in x[1:]:
#		c = [i, c]
#	return c


for path, dirs, files in os.walk(idir):
	for f in files:
		if ".txt" in f:
			tmp = io.open(path + "//" + f, "r", encoding = "utf-8")
			Info.update([((path.split("www")[-1] + "//" + f), tmp.readlines())])
			tmp.close()

	Dirs.append(path)
	files = [ f for f in files if ".txt" not in f ]
	Files.append(map((path.split("www")[-1] + "//").__add__ ,files))

files = []
map(files.extend, Files)

pattern_style = """\
	font-size: 14pt;
	color: black;
	white-space: pre;
"""

pattern = """\
<p style = \"{style}\">\
{index}{fill_symbol}\
<a href=\"{file}\" style = \"color: black;\"> {info} </a>
	</p>

	""".format(
	style = pattern_style,
	index = "{index}",
	fill_symbol = "\t",
	file = "{file}",
	info = "{info}")

#Q = F([string.split, ["/", "//"].__add__, reversed, string.replace])

tmp1 = "\n".join(
[
pattern.format(
	index = ind,
	file = file,
	info = file.replace("/static/models/", "")
) for ind, file in enumerate(map(F(
	[
		string.split,
		["/", "//"].__add__,
		reversed,
		string.replace
	]
).getf2(), files))])



tmp2 = "".join(
[
"<p style = \"white-space: pre; font-size: 14pt;\"><b>{img}:</b>\n\t{msg}</p>".format(
	img = img,
	msg = "\t".join(msg)) for img, msg in sorted(Info.items())])

tmp = """\
Content-type: text/html\n
<!DOCTYPE HTML>
<html>
<head>
	<meta charset = "utf-8">
	<title>Models Images</title>
</head>
<body>
	<h1>Imgs: [Dir: {idir}]</h1>

	<hr>
	<br>

	{img_content}

	<br>
	<hr>
	<br>

	{img_info}

	<br>
	<hr>

</body>
</html>
""".format(
	idir = hrefdir,
	img_content = tmp1,
	img_info = tmp2
)


print tmp

