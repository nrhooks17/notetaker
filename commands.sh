#!/bin/bash

read -r -d '' HELP << EOM
usage notetaker <command>

bash                : bash into the app container
bash-react          : bash into the react app container
up                  : start the app
build               : build and start the app
down                : stop the app
db                  : bash into the db container
EOM

function notetaker() {
  if [[ "$1" == "bash" ]]; then
    docker exec -it notetaker-app-1 /bin/bash
  elif [[ "$1" == "bash-react" ]]; then
    docker exec -it notetaker-react-app-1 /bin/bash
  elif [[ "$1" == "up" ]]; then
    docker compose up
  elif [[ "$1" == "build" ]]; then
    docker compose up --build
  elif [[ "$1" == "down" ]]; then
    docker compose down
  elif [[ "$1" == "db" ]]; then
    docker exec -it notetaker-mongo-1 mongo
  else
       echo $HELP
  fi
}