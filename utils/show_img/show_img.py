#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import os
import io
import PIL.Image
import aalib
import sys

Info = "Print image on terminal (aalib)."

img_path = ""
width = 80
height = 40
DefaultRender = "ansi"
render_types = [ "linux", "ascii", "ansi" ]
renders = [ aalib.LinuxScreen, aalib.AsciiScreen, aalib.AnsiScreen ]
renders = dict([ ( v, renders[i] ) for i, v in enumerate(render_types) ])
aarender = ""
Screen = None

parser = argparse.ArgumentParser(description = Info)
parser.add_argument("--image-path", "-i", action = "store", dest = "arg_img",
		type = str, nargs = "?", help = "--image-path[or -i] <path to image file>")
parser.add_argument("--width", "-W", action = "store", dest = "arg_w",
		type = str, nargs = "?", help = "--width[or -W] <aalib screen width>")
parser.add_argument("--height", "-H", action = "store", dest = "arg_h",
		type = str, nargs = "?", help = "--height[or -H] <aalib screen height>")
parser.add_argument("--full-screen", "-F", action = "store_true", dest = "arg_f",
		help = "--full-screen[or -F] <enable full screen mode>")
parser.add_argument("--auto-size", "-A", action = "store_true", dest = "arg_a",
		help = "--auto-size[or -A] <auto set up aalib screen size>")
parser.add_argument("--debug-mode", "-d", action = "store_true", dest = "arg_debug",
		help = "--debug-mode[or -d] <print debug information>")
parser.add_argument("--render", "-r", action = "store", dest = "arg_render",
		type = str, nargs = "?", help = "--render[or -r] (ansi|ascii|linux) <set type of aalib render>")
args = parser.parse_args()

if args.arg_img == None or args.arg_img == "":
	print "Empty image path"
	sys.exit(0)
else:
	img_path = args.arg_img


if args.arg_render != None and args.arg_render != "":
	if args.arg_render.lower() not in render_types:
		print "Invalid rendor type: {0}\nOnly this types allowed: {1}, {2}, {3}".format(args.arg_render, )
		sys.exit(0)
	else:
		aarender = args.arg_render.lower()
else:
	aarender = DefaultRender
Screen = renders[aarender]

if args.arg_w != None and args.arg_w != "":
	width = int(args.arg_w)

if args.arg_h != None and args.arg_h != "":
	height = int(args.arg_h)

if args.arg_f:
	rows, columns = os.popen("stty size", "r").read().split()
	width = int(columns)
	height = int(rows)


flagd = args.arg_debug

if not args.arg_a:
	if flagd:
		print "Screen size: {0}x{1}\n".format(width, height)
#	screen = aalib.AsciiScreen(width = width, height = height)
#	screen = aalib.LinuxScreen(width = width, height = height)
#	screen = aalib.AnsiScreen(width = width, height = height)
	screen = Screen(width = width, height = height)
	image = PIL.Image.open(img_path).convert("L").resize(screen.virtual_size)
	screen.put_image((0, 0), image)
	print screen.render()
	niw, nih = image.size
	iw, ih = PIL.Image.open(img_path).size
	vw, vh = screen.virtual_size
	rw, rh = screen.render_size
	coeff = max([ iw/niw, ih/nih ])
	rows, columns = os.popen("stty size", "r").read().split()
	pass
	if flagd:
		print "\n\nOriginal image size(points): {0}x{1}".format(iw, ih)
		print "Aalib render size: {0}x{1}".format(rw, rh)
		print "Aalib screen virtual size: {0}x{1}".format(vw, vh)
		print "Coeff: {0}".format(coeff)
		print "New image size(points): {0}x{1}".format(niw, nih)
		print "Terminal size(columns x rows): {0}x{1}".format(columns, rows)
		print "Render screen type: {0}".format(aarender)
else:
#	rows, columns = os.popen("stty size", "r").read().split()
#	image = PIL.Image.open(img_path).convert("L")
#	iw, ih = image.size
#	rw, rh = (width, height)
#	screen = aalib.AnsiScreen(width = width, height = height)
#	vw, vh = screen.virtual_size
#	coeff = max([ iw/vw, ih/vh ]) + 1
#	niw, nih = ( int(iw/coeff), int(ih/coeff) )
#	image = image.resize(( niw, nih ))
#	screen.put_image((0, 0), image)
#	print screen.render()
	rows, columns = os.popen("stty size", "r").read().split()
	rw, rh = (width, height)
	vw, vh = rw*2, rh*2
	image = PIL.Image.open(img_path).convert("L")
	iw, ih = image.size
	coeff = iw/ih
	rh = rw/2*coeff
	while True:
		if rh > rows:
			rh = rows
			rw = 2*rh/coeff
		if rw > columns:
			rw = rh
			rh = rw/2*coeff
		if rh <= rows and rw <= columns:
			break
	width = rw
	height = rh
#	screen = aalib.AnsiScreen(width = width, height = height)
	screen = Screen(width = width, height = height)
	image = PIL.Image.open(img_path).convert("L").resize(screen.virtual_size)
	niw, nih = image.size
	vw, vh = screen.virtual_size
	screen.put_image((0, 0), image)
	print screen.render()
	pass
	if flagd:
		print "\n\nOriginal image size(points): {0}x{1}".format(iw, ih)
		print "Aalib render size: {0}x{1}".format(rw, rh)
		print "Aalib screen virtual size: {0}x{1}".format(vw, vh)
		print "Coeff: {0}".format(coeff)
		print "New image size(points): {0}x{1}".format(niw, nih)
		print "Terminal size(columns x rows): {0}x{1}".format(columns, rows)
		print "Render screen type: {0}".format(aarender)
