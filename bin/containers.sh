#!/bin/bash

start_containers()
{
	sudo docker run --name rift-db -p 27017:27017 -d mongo
	sudo docker run --name rift-mq -p 5672:5672 -p 15672:15672 -e RABBITMQ_PASS="password" -d tutum/rabbitmq
}
stop_containers()
{
	sudo docker kill rift-db
	sudo docker kill rift-mq
}

case "$1" in
  start)
    start_containers
    ;;
  stop)
    stop_containers
    ;;
  *)
    echo "Usage: start_containers.sh {start|stop}"
    exit 1
esac