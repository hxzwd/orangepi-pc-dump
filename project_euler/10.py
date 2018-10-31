#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import copy
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])

lim = 2*(10**6)
pos = 10001

res = None
tmp = None


def primes_e(n):
	primes = [ ]
	multiples = []
	for i in xrange(2, n + 1, 1):
		if i not in multiples:
			primes.append(i)
			multiples.extend(xrange(i * i, n + 1, i))
	return ( primes, multiples )


def eratosfen0(n):
	primes = []
	k = 0
	for i in xrange(2, n + 1):
		for j in xrange(2, i):
			if i % j == 0:
				k += 1
		if k == 0:
			primes.append(i)
		else:
			k = 0
	return primes


def eratosfen1(n):
	primes = []
	for i in xrange(2, n + 1):
		for j in xrange(2, i):
			if i % j == 0:
				break
		else:
			primes.append(i)
	return primes



def eratosfen2(n):
	primes = []
	for i in xrange(2, n + 1):
		for j in primes:
			if i % j == 0:
				break
		else:
			primes.append(i)
	return primes



def eratosfen3(n):
	primes = []
	for i in xrange(2, n + 1):
		for j in primes:
			if j > int(sqrt(i) + 1):
				primes.append(i)
				break
			if i % j == 0:
				break
		else:
			primes.append(i)
	return primes



def eratosfen4(n):
	primes = []
	for i in xrange(2, n + 1):
		if i > 10:
			if i % 2 == 0 or i % 10 == 5:
				continue
		for j in primes:
			if j > int(sqrt(i) + 1):
				primes.append(i)
				break
			if i % j == 0:
				break
		else:
			primes.append(i)
	return primes



def eratosfen5(n):
	primes = []
	for i in xrange(3, n + 1, 2):
		if i > 10:
			if i % 2 == 0 or i % 10 == 5:
				continue
		for j in primes:
			if j > int(sqrt(i) + 1):
				primes.append(i)
				break
			if i % j == 0:
				break
		else:
			primes.append(i)
	return primes



def eratosfen(n):
	primes = []
	for i in xrange(3, n + 1, 2):
		if i > 10:
			if i % 2 == 0 or i % 10 == 5:
				continue
		for j in primes:
			if j * j - 1 > i:
				primes.append(i)
				break
			if i % j == 0:
				break
		else:
			primes.append(i)
	return [ 2 ] + primes

#for i in nums:
#	if max(tmp) >= i and i in tmp:
#		tmp = filter(lambda x: x % i != 0 or x == i, tmp)
#	else:
#		break


#res = primes_e(lim)[0]


#print res[10000]


tmp = eratosfen(lim)
res = sum(tmp)

print res

