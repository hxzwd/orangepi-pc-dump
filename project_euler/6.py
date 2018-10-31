#!/usr/bin/env python

#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from math import *

print "Project euler\nProblem:\t{0}\n".format(sys.argv[0].strip("./").split(".")[0])


res = 0

res = -sum([ i**2 for i in range(1, 101) ]) + sum(range(1, 101))**2


print res


