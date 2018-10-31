#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])


num = 600851475143
tmp = num
fact = []

for i in range(2, int(sqrt(num))):
	if i > tmp:
		break
	if tmp % i == 0:
		fact.append(i)
		tmp = tmp / i

res = fact[-1]

print res


