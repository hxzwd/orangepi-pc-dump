#!/bin/bash


CURR_DIR="$(pwd)"
PROG_DIR="/home/hjk/net_dir/netcat_test"
PROG="netcat_server.sh"



$PROG_DIR/./$PROG > /dev/null 2> /dev/null &



