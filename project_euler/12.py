#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import string
import copy
import itertools
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])


res = None

divisors = lambda n: sorted(reduce(list.__add__, [ [d, n / d] for d in xrange(1, int(sqrt(n))) if n % d == 0 ]))

def factor(n):
	fact = []
	d = divisors(n)
	tmp_ = n
	for i in d[1:]:
		if tmp_ < i:
			break
		while tmp_ % i == 0:
			fact.append(i)
			tmp_ = tmp_ / i
	return fact


def triangle(n):
	nums = [ sum(list(xrange(1, i + 1))) for i in xrange(1, n + 1, 1) ]
	return nums



def triangle_(n0, n, m):
	misc = []
	x = sum(list(xrange(1, n0)))
	for i in xrange(n0, n + 1, 1):
		x += n0
		d = divisors(x)
		if len(d) > m:
			return [ x, i, d ]
		else:
			misc.append([ i, len(d) ])
	return misc

print res
