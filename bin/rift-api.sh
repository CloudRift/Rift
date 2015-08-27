#!/bin/bash

start_containers()
{
  docker build -t rift .
  docker run --name rift-api --link rift-mq:mq --link rift-db:db  -p 127.0.0.1:8000:8000 -d rift \
  gunicorn -b '0.0.0.0:8000' rift.app:application
}
stop_containers()
{
  docker kill rift-api
  docker rm rift-api
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
    echo "Usage: rift.sh {start|stop|restart}"
    exit 1
esac
