
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


import os
import re
import io
import sys


import linecache
import multiprocessing

from multiprocessing.dummy import Pool as ThreadPool


dataPath = "/home/hjk/dump_dir/arc_data/arc1_txt_part"
db = []


def get_files_list(path, mask = "^[0-9]*\.txt$"):
	if mask:
		mask = re.compile(mask)
	files1 = filter(mask.match, sorted(os.listdir(path)))
	files2 = [ os.path.join(dataPath, fn) for fn in files1 ]
	return files1, files2



def get_params_list(testfile, path = ""):
	if not os.path.isabs(testfile):
		testfile = os.path.join(path, testfile)
	lines = []
	with io.open(testfile, "r", encoding = "utf-8") as fn:
		for i, line in enumerate(fn):
			if re.match(r"^\s*$", line):
				break
			else:
				lines.append((i, line.strip().split(";")[0]))
		fn.close()
	return lines, len(lines)


def read_files_in_memory(files, path = ""):
	if path != "":
		files = [ os.path.join(path, fn) for fn in files ]
	global db
	old_files = [ data[0] for data in db ]
	files = [ fn for fn in files if fn not in old_files ]
	for fn in files:
		with io.open(fn, "r", encoding = "utf-8") as handle:
			db.append((os.path.basename(fn), handle.readlines()))
			handle.close()
	return db


def get_files_lines(files, path = ""):
	if path != "":
		files = [ os.path.join(path, fn) for fn in files ]
	ln = []
	for fn in files:
		with io.open(fn, "r", encoding = "utf-8") as handle:
			ln.append((os.path.basename(fn), len(handle.readlines())))
			handle.close()
	return ln


def split_by_cells(data, ln, lc):
	l1 = range(0, ln - lc + 1, lc)
	l2 = range(lc, ln + 1, lc)
	ll = zip(l1, l2)
	data = [ data[i[0]:i[1]] for i in ll ]
	return data


def map_function(filename):
	print filename + "\n"
	cells = []
	data = []
	with io.open(filename, "r", encoding = "utf-8") as handle:
		data = handle.readlines()
		handle.close()
	return data[0::16]




def test_function_1(files, n = -1):
	return [ map_function(fn) for fn in files[0:n] ]


def test_function_2(files, n = -1, pn = 2):
	pool = ThreadPool(pn)
	res = pool.map(map_function, files[0:n])
	pool.close()
	pool.join()
	return res



def map_function_2(cell_data):
	cell_coords = re.findall(r"[0-9]{2}\-[0-9]{2}", cell_data[0])[0]
	return cell_coords


def print_file_total_lines(filename):
	if not os.path.isabs(filename):
		total_lines = -1
	with io.open(filename, "r", encoding = "utf-8") as handle:
		total_lines = len(handle.readlines())
		handle.close()
	print "{0}:\t{1}".format(filename, total_lines)
	return total_lines


_, files = get_files_list(dataPath)
file1, file2 = files[0:2]


pool = multiprocessing.Pool(processes = 4)
res = pool.map(map_function, files[0:4])

sys.exit()

#print_file_total_lines(file1)
#print_file_total_lines(file2)

#sys.exit()

p1 = multiprocessing.Process(target = print_file_total_lines, args = (file1, ))
p2 = multiprocessing.Process(target = print_file_total_lines, args = (file2, ))

p1.start()
p2.start()

p1.join()
p2.join()

sys.exit()


params = get_params_list(files[0])
lines_for_cell = params[1] + 1


db = read_files_in_memory(files[0:1])
ln = get_files_lines(files[0:1])


lines_for_file = ln[0][1]



data = split_by_cells(db[0][1], lines_for_file, lines_for_cell) 


test_ = lambda x: [ map_function_2(i) for i in x ]

def test():
	pool = ThreadPool(4)
	res = pool.map(map_function_2, data)
	pool.close()
	pool.join()
	return res

sys.exit()

files = files[0:2]


pool = ThreadPool(2)

res = pool.map(map_function, files)

pool.close()
pool.join()



