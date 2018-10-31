#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])

res = None

for a in xrange(1, 1000):
	for b in xrange(1, 1000):
		c = sqrt(a**2 + b**2)
		if modf(c)[0] != 0.0:
			continue
		c = int(c)
		if a + b + c == 1000:
			res = [a, b, c]
			break

res = reduce(int.__mul__, res)

print res


