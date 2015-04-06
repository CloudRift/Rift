#!/bin/bash

start_worker()
{
    gunicorn -b '127.0.0.1:8001' rift.api.worker.app:application &
    celery worker -A rift.api.worker.app
}

stop_worker()
{
    pkill gunicorn
}

case "$1" in
  start)
    start_worker
    ;;
  stop)
    stop_worker
    ;;
  *)
    echo "Usage: rift-worker.sh {start|stop}"
    exit 1
esac
