#!/bin/bash

start_app()
{
    gunicorn rift.app:application
}

stop_app()
{
    pkill gunicorn
}

case "$1" in
  start)
    start_app
    ;;
  stop)
    stop_app
    ;;
  *)
    echo "Usage: rift.sh {start|stop}"
    exit 1
esac
