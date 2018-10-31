#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import os
import io
import re
import sys

import urllib2



url = "https://time100.ru/timestamp"
pattern = r"(\<strong\>)([0-9]+)(\</strong\>)"
timezone = "Europe/Moscow"
#timezone = "Etc/UTC"

page = urllib2.urlopen(url)
content = page.read()
page.close()

timestamp = re.findall(pattern, content)[0][1]

if "-h" in sys.argv:
	print "Usage: get_timestamp [OPTIONS]"
	print
	print "Option\t\tMeaning"
	print " -h\t\tShow help"
	print " -q\t\tQuiet mode"
	print " -s\t\tSet system date from timestamp"
	sys.exit(0)


if "-s" not in sys.argv:
	if "-q" not in sys.argv:
		print "Timezone is {0}".format(timezone)
		print "Timestamp[from {0}]:\n".format(url)
	print timestamp
else:
	os.system("sudo ln -sf /usr/share/zoneinfo/{0} /etc/localtime".format(timezone))
	os.system("sudo date +%s -s @{0}".format(timestamp))
