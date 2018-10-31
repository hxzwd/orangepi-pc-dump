#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2
import argparse
import os
import io
import PIL.Image
import sys

Info = "Get image from url tool."
DefaultImagePath = "/home/hjk/images"
DefaultImageName = "get_img_image"
DefaultImageExtension = "png"
img_name = ""
img_dir = ""

parser = argparse.ArgumentParser(description = Info)
parser.add_argument("--url", "-u", action = "store", dest = "arg_url",
		type = str, nargs = "?", help = "--url[or -u] <image internet location>")
parser.add_argument("--name", "-n", action = "store", dest = "arg_name",
		type = str, nargs = "?", help = "--name[or -n] <image output name>")
parser.add_argument("--dir", "-d", action = "store", dest = "arg_dir",
		type = str, nargs = "?", help = "--dir[or -d] <image save dir>")
parser.add_argument("--ext", "-e", action = "store", dest = "arg_ext",
		type = str, nargs = "?", help = "--ext[or -e] <image save extension>")
args = parser.parse_args()

if args.arg_url == None or args.arg_url == "":
	print "Empty image URL"
	sys.exit(0)

if args.arg_name == None or args.arg_name == "":
	img_name = DefaultImageName
else:
	img_name = args.arg_name

if args.arg_dir == None or args.arg_dir == "":
	img_dir = DefaultImagePath
else:
	img_dir = args.arg_dir

if args.arg_ext == None or args.arg_ext == "":
	img_ext = DefaultImageExtension
	tmp = args.arg_url.split(".")
	if len(tmp) >= 2:
		img_ext = tmp[-1]
else:
	img_ext = args.arg_ext


tmp = img_name.split(".")
if len(tmp) < 2:
	img_name += "." + img_ext

img_save_path = img_dir + "//" + img_name

img_frame = io.BytesIO(urllib2.urlopen(args.arg_url).read())
image = PIL.Image.open(img_frame)
image.save(img_save_path)

print "Image from URL: {0} saved in {1}".format(args.arg_url, img_save_path)

