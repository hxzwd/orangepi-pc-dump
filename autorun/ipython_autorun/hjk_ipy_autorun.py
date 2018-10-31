#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import sys
import IPython
#import io
#import time

print "SYS AND OS IMPORTED"
HJKAUTORUNFILE = __file__
print "__file__ is {}".format(__file__)

HJKRUNFILE = ""
HJKIPY = IPython.get_ipython()
global HJKIPYARGS
if HJKIPYARGS != None:
	if "-i" in HJKIPYARGS:
		EXCP = None
		try:
			HJKRUNFILE = HJKIPYARGS[HJKIPYARGS.index("-i") + 1]
		except Exception as EXCP:
			HJKRUNFILE = ""

def Doc(obj):
	print obj.__doc__

def Nano(x = None):
	if (x == "" or x == None) and HJKRUNFILE != "":
		x = HJKRUNFILE
	os.system("nano " + x)

def Cpu(l = False):
	from io import open
	from time import sleep
	while True:
		f = open("/sys/class/thermal/thermal_zone0/temp", "r")
		temp = f.read()
		f.close()
		print "Cpu temp:\t\t{0} 'C".format(int(temp)/1000.0)
		if not l:
			break
		sleep(1)


def Run(x = "", t = False):
	if (x == "" or x == None) and HJKRUNFILE != "":
		x = HJKRUNFILE
	HJKIPY.run_line_magic("run", t*"-t " + x)

def IPythonArgs():
	print eval("\"Arguments:\\n\" + " + "(\"{:>20}\\n\"*len(HJKIPYARGS))" +
	".format" + str(tuple(HJKIPYARGS)))


def EditAutorun():
	Nano(HJKAUTORUNFILE)

HJKIMPORTS = [ "os", "sys", "IPython" ]

HJKFUNCS = [ "Doc", "Nano", "Info", "Cpu", "EditAutorun", "IPythonArgs" ]

def Info():
	print "Profile:\t\t{0}\n\
Imported packages:\t\t{1}".format("hjk", " ".join(HJKIMPORTS))
	print eval("\"Funcs:\\n\" + " + "(\"{:>10}\\n\"*len(HJKFUNCS))" +
		".format" + str(tuple(HJKFUNCS)))
	IPythonArgs()

