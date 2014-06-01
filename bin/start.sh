#!/bin/bash
######################################################################
# Server Start Script
#
# Project: Code Review
# By:      Steamed Pears
#
# This script should start a server serving the front and back ends 
# via node.
######################################################################

source bin/helpers.sh
ROOT_DIR=`pwd`
TIME=`timestamp`

######################################################################
# Configuration

VIRTUALENV=$ROOT_DIR/src/server/develop
UWSGI=uwsgi

if $PROD; then
  PORT=25414
else
  PORT=8000
  echo "Starting development server at http://localhost:$PORT/index.html"
  CLIENT_DIR=$ROOT_DIR/src/client
  OPTS="--check-static $CLIENT_DIR"
fi

SERVER_PID=$ROOT_DIR/var/server.pid
SERVER_LINK=$ROOT_DIR/var/server.log
SERVER_LOG=$ROOT_DIR/var/logs/server
SERVER_DIR=$ROOT_DIR/src/server

INDEX_SCRIPT=$SERVER_DIR/index.py

######################################################################
# Silently stop server, in case it's running
bin/stop.sh &> /dev/null

######################################################################
# Server initialization

cd $SERVER_DIR
source $VIRTUALENV/bin/activate
$UWSGI --master --http :$PORT --wsgi-file $INDEX_SCRIPT --virtualenv $VIRTUALENV $OPTS --pidfile $SERVER_PID &> $SERVER_LOG.$TIME.log &
ln -s -f $SERVER_LOG.$TIME.log $SERVER_LINK
