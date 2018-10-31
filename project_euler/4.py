#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import itertools
import string
import copy
from math import *

print sys.argv

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])


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


group_ = lambda func, lst: [ filter(func, lst), filter(lambda x: not func(x), lst) ]

def group(func, lst):
	if type(func) is not list:
		groups = group_(func, lst)
	else:
		groups = [ group_(f, lst)[0] for f in func ] + [ group_(lambda x: not reduce(lambda a, b: a or b, [ f(x) for f in func ]), lst)[0] ]
#		return [ i for i in groups if i != [] ]
	for i, val in enumerate(groups):
		if val == []:
			groups[i] = [1]
	return groups

def filter_replace(func, lst, repl):
	tmp_ = lst
	for i, v in enumerate(lst):
		if func(v):
			tmp_[i] = repl
	return tmp_

res = None

#nums1 = [100, 100]
#nums2 = [999, 999]
#num1 = reduce(int.__mul__, nums1)
#num2 = reduce(int.__mul__, nums2)
#nums = [ i for i in map(str, range(num1, num2)) if i == "".join(reversed(i)) ]

#for i in range(num1, num2):
#	break


tmp = list(map(list, itertools.product(string.digits, repeat = 2)))[10:]
tmp = [ [ i + [j, j] + list(reversed(i)) for j in string.digits ] for i in tmp ]
tmp = list(filter(lambda x: x <= 999**2, map(lambda x: int("".join(x)), reduce(list.__add__, tmp))))

data = []

for i, n in enumerate(tmp):
	max_divisor = max(filter(lambda x: x < 999, divisors(n)))
	for k in range(100, max_divisor + 1):
		if n % k == 0 and n / k > 99 and n / k < 999:
			res = [ n, k, n / k ]
			break

print res

sys.exit(0)

for i, n in enumerate(reversed(tmp)):
#	fact = factor(n)
#	fact = reduce(int.__mul__, filter(lambda x: x < 100, fact))
	groups = group([ lambda x: x < 100, lambda x: x > 999 ], factor(n))
	res = [ copy.deepcopy(groups) ]
	if groups[1] != [1]:
		continue
	groups[0] = reduce(int.__mul__, groups[0])
	groups = filter_replace(lambda x: x > 99 and x < 999, [ groups[0] ] + groups[-1], None)
	data.append(groups)
	if len(groups) == 2 and not None in groups:
		res.append((groups, i, n))
		break
#	if groups[1] != []:
#		continue
#	if groups[0] == []:
#		if len(groups[-1]) == 2:
#			res = (n, groups[-1])
#			break
#		else:
#			continue
#	else:
#		groups[0] = reduce(int.__mul__, groups[0])
#	if True in map(lambda x: x > 999, fact):
#		continue
#	else:
#		pass
#	d = filter(lambda x: x > 99, d)
#	if len(d) >= 2:
#		res = d
#		break



print res


