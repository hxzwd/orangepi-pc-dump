#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import string
import copy
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])


res = None

f = open("8.txt", "r")
data = [ int(i) for i in f.read() if i in string.digits  ]
f.close()

#print data
#print len(data)

#zind = [ i for i, v in enumerate(data) if v == 0 ]
#zind = [ zind[0] ] + [ v for i, v in enumerate(zind[1:]) if zind[i] + 13 < v ]
tmp = copy.deepcopy(data)

c = "".join(map(str, data))
cc = [ c[i:j] for i, j in zip(xrange(0, 1000 - 50, 50), xrange(49, 1000, 50)) ]


m = "".join(map(str, tmp))
mm = [ m[i:j] for i, j in zip(xrange(0, 1000 - 50, 50), xrange(49, 1000, 50)) ]
mm_ = [ i for i in "".join(mm).split("0") if i != "" ]


tmp_ = [ data[i:j] for i, j in zip(xrange(0, 1000 - 13, 1), xrange(13, 1001, 1)) if not 0 in data[i:j] ]
l = list(map(lambda x: reduce(lambda a, b: a * b, map(int, x)), tmp_))

#for i in zind:
#	if i + 13 <= len(data) - 1:
#		tmp[i - 12:i + 13] = len(data[i - 12:i + 13]) * [0]
#	else:
#		tmp[i - 12:] = len(data[i - 12:]) * [0]

#l = filter(lambda x: len(x) > 12, [ i for i in "".join(map(str, tmp)).split("0") if i != "" ])
#l = list(map(lambda x: [ int(i) for i in x ], l))
#ll = copy.deepcopy(l)
#ll = [ [ v[j:j + 13] for j in range(0, len(v) - 13 + 1) ] for v in ll ] 
#l = list(map(lambda x: reduce(int.__mul__, x), reduce(list.__add__, [ [ v[j:j + 13] for j in range(0, len(v) - 13 + 1) ] for v in l ])))

res = max(l)

print res


