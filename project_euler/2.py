#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals


print "Project euler\nProblem:\t2\n"

res = 0
i1 = 1
i2 = 1
fib = [i1, i2]


while res <= 4000000:
	res = i2 + i1
	i1 = i2
	i2 = res
	fib.append(i2)

res = filter(lambda x: not x % 2, fib)
res = sum(res)

print res


