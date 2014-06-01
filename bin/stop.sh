#!/bin/bash
######################################################################
# Server Stop Script
#
# Project: Code Review
# By:      Steamed Pears
#
# This script should kill node and redis-server.
######################################################################

ROOT_DIR=`pwd`

######################################################################
# Configuration

SERVER_PID=$ROOT_DIR/var/server.pid
#DB_PID=$ROOT_DIR/var/db.pid

######################################################################
# Stop server and db

kill -QUIT $(< $SERVER_PID)
if [[ $? -eq 0 ]]; then
  sleep 2
fi
#kill -SIGTERM $(< $DB_PID)
