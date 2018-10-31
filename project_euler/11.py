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

f = open("11.txt", "r")
c = f.read().replace("\n", " ").split(" ")[:-1]
data = list(map(int, c))
f.close()

pos = None

def subseq(i, j, n = 20, m = 20):
	coords = []
	ij = []
	ii = [ i ] * 4
	jj = [ j ] * 4
	[ iip, iim, jjp, jjm ] = list(map(list, reduce(list.__add__, [ [ xrange(z, z + x, y) for x, y in [ (4, 1), (-4, -1) ] ] for z in [ i, j ] ])))
	pos = [ [ ii, iip, iim ], [ jj, jjp, jjm ] ]
	I, J = pos
	I_, J_ = list(map(lambda x: x[1:], pos))
#	I, J = list(map(lambda x: x[1:], pos))
	coords = filter(lambda x: x[0] in I and x[1] in J, list(map(list, list(itertools.combinations(reduce(list.__add__, pos), 2)))))
	coords.remove([ii, jj])
#	coords = [ list(map(list, zip(x, y))) for x, y in coords ]
	coords = [ zip(x, y) for x, y in coords if not True in map(lambda x: x < 0 or x >= n, x + y) ]
	return coords, pos

def get_values(arr, coords):
	values = []
	tmp_ = []
	for seq in coords:
		tmp_ = []
		for i, j in seq:
			tmp_.append(arr[i][j])
		values.append(tmp_)
	return values


tmp = copy.deepcopy(data)
m = copy.deepcopy(c)

cc = [ " ".join(c[i:j]).strip() for i, j in zip(xrange(0, 400 - 19, 20), xrange(20, 420, 20)) ]

m = [ data[i:j] for i, j in zip(xrange(0, 400 - 19, 20), xrange(20, 420, 20)) ]
mm = [ c[i:j] for i, j in zip(xrange(0, 400 - 19, 20), xrange(20, 420, 20)) ]


res = []

for i in range(0, 20):
	for j in range(0, 20):
		coords = subseq(i, j)
		res.append(get_values(m, coords[0]))

res_ = copy.deepcopy(res)
tmp = reduce(list.__add__, res)
tmp_ = list(map(lambda x: reduce(int.__mul__, x), tmp))




res = max(tmp_)

print res


