#!/bin/bash

# start docker
echo "Starting docker using the command 'sudo systemctl start docker'"
sudo systemctl start docker
echo "Docker is now runinng"

# start pycharm and webstorm
echo "starting pycharm"
/home/centralstation/.local/share/JetBrains/Toolbox/scripts/pycharm &
echo "pycharm is now running"

echo "sleeping for 5 seconds"
sleep 5

echo "starting webstorm"
/home/centralstation/.local/share/JetBrains/Toolbox/scripts/webstorm &
echo "webstorm is now running"


# go into the python directory
echo "moving into the notetaker project directory"
cd /opt/webapps/python/projects/notetaker

# source the notetaker project commands
echo "sourcing project commands for notetaker"
source /opt/webapps/python/projects/notetaker/commands.sh

# start the docker container
echo "building the notetaker project"
notetaker build

