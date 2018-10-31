#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
import os
import sys
import socket
import threading
import time

HOST = "192.168.0.106"
HOSTMASK = "192.168.0.{}"
PORT = 9090
PACK_SIZE = 512

print "Netowed signals send: main_send.py\n"
print "\"{0}:{1}\"\t\t\t[HOST:PORT]\n\
{2}\t\t\t[PACK_SIZE]\n".format(
	HOST, PORT, PACK_SIZE)


width, height = os.popen("stty size", "r").read().split()
print width, height
print __file__


LOCALHOST = os.popen("ip addr | grep 192.168.0.[0-9]* -o", "r").read().split()[0]
HOSTS = [ HOSTMASK.format(i) for i in range(100, 120) ]
HOSTS.remove(LOCALHOST)

THREADS = []
SOCKETS = []

FLAG_END = False
MAINHOST = ""

print "LOCALHOST:\t\t\t{0}".format(LOCALHOST)

def worker(sock, host, port):
	try:
		sock.connect( (host, port) )
		data = sock.recv(PACK_SIZE)
		print data
		sock.send("orange {0}".format(LOCALHOST))
		FLAG_END = True
		MAINHOST = data
	except Exception as excp:
		print "Can`t reach {0}:{1}".format(host, port)
	while True:
		pass

for host in HOSTS:
	sock = socket.socket()
	thr = threading.Thread(target = worker, args = (sock, host, PORT, ))
	thr.start()
	THREADS.append(sock)
	SOCKETS.append(sock)



time.sleep(5)
while True:
	if FLAG_END:
		print MAINHOST
		for thr in THREADS:
			thr._Thread_stop()
		for sock in SOCKETS:
			sock.close()
		break
	else:
		time.sleep(1)






