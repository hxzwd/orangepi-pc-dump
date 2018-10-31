#!/usr/bin/python2.7


import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

file_name = "test.png"
img_dir = "imgs"

x = [1, 2, 3]
y = [1, 0, 1]

plt.plot(x, y)
plt.savefig(img_dir + "//" + file_name)
print "Figure saved in file: {0}\n".format(img_dir + "//" + file_name)

