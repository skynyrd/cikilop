#!/usr/bin/env sh

ClearEnvironment(){
    docker rmi -f $(docker images | grep '^<none>' | awk '{print $3}')
    docker rmi -f $(docker images | grep cikilop | awk '{print $3}')
    docker rm -f $(docker ps -a | grep cikilop_cikilop | awk '{print $1}')
}

ClearEnvironment

docker-compose up --abort-on-container-exit

if [ $? = 0 ]; then
  echo "Successfull build..."
  docker build -t skynyrd/cikilop:latest -t skynyrd/cikilop:1.0 .
#  docker push skynyrd/cikilop
  exit 0
else
  echo "Process failed..."
  exit 1
fi