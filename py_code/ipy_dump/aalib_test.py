#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import urllib2
import PIL.Image
import aalib
import sys

img_url = "https://www.python.org/static/favicon.ico"
img_url = "https://sun9-1.userapi.com/c840627/v840627124/84c50/J22i_TvNUqQ.jpg"

if len(sys.argv) > 1:
	img_url = sys.argv[1]

print "Image location: {0}".format(img_url)

if True:
	screen = aalib.AsciiScreen(width = 80, height = 40)
	fp = io.BytesIO(urllib2.urlopen(img_url).read())
	image = PIL.Image.open(fp).convert("L").resize(screen.virtual_size)
	screen.put_image((0, 0), image)
	print screen.render()
else:
	image_dir = "imgs"
	image_file = "test.png"
	image_path = image_dir + "//" + image_file
	width = 80
	height = 40
	screen = aalib.AsciiScreen(width = width, height = height)
	image = PIL.Image.open(image_path).convert("L").resize(screen.virtual_size)
	screen.put_image((0, 0), image)
	print screen.render()





