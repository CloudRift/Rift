#!/bin/bash

start_containers()
{
  docker run --name rift-db -p 127.0.0.1:27017:27017 -d mongo
  docker run --name rift-mq -p 127.0.0.1:5672:5672 -p 15672:15672 -e RABBITMQ_PASS="password" -d tutum/rabbitmq
}
stop_containers()
{
  docker kill rift-db
  docker kill rift-mq
  docker rm rift-db
  docker rm rift-mq
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
    echo "Usage: containers.sh {start|stop|restart}"
    exit 1
esac
