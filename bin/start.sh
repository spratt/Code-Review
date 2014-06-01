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
  CONF_FILE=$ROOT_DIR/etc/prod.ini
  OPTS="--pidfile $ROOT_DIR/var/server.pid"
  OPTS="$OPTS --chdir $ROOT_DIR/src/server"
else
  CONF_FILE=$ROOT_DIR/etc/dev.ini
  OPTS="--check-static $ROOT_DIR/src/client"
  OPTS="$OPTS --pidfile $ROOT_DIR/var/server.pid"
  OPTS="$OPTS --chdir $ROOT_DIR/src/server"
fi

SERVER_LINK=$ROOT_DIR/var/uwsgi.log
SERVER_LOG=$ROOT_DIR/var/logs/uwsgi
SERVER_DIR=$ROOT_DIR/src/server

######################################################################
# Silently stop server, in case it's running
bin/stop.sh &> /dev/null

######################################################################
# Server initialization

source $VIRTUALENV/bin/activate
$UWSGI $CONF_FILE $OPTS &> $SERVER_LOG.$TIME.log &
ln -s -f $SERVER_LOG.$TIME.log $SERVER_LINK
