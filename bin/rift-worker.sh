#!/bin/bash

start_containers()
{
  docker build -t rift .
  docker run --name rift-worker --link rift-db:db --link rift-mq:mq -p 127.0.0.1:8001:8001 -d rift \
  su -m rift-worker -c "gunicorn -b '0.0.0.0:8001' rift.api.worker.app:application & celery worker -A rift.api.worker.app"
}
stop_containers()
{
  docker kill rift-worker
  docker rm rift-worker
}

case "$1" in
  start)
    start_containers
    ;;
  stop)
    stop_containers
    ;;
  restart)
    stop_containers
    start_containers
    ;;
  *)
    echo "Usage: rift-worker.sh {start|stop|restart}"
    exit 1
esac
