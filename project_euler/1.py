#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals


print "Project euler\nProblem:\t1\n"

res = 0

for i in range(1, 1000):
	if i % 3 == 0 or i % 5 == 0:
		res += i

print res

