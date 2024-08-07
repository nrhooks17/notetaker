#!/bin/bash

# start docker
echo "Starting docker using the command 'sudo systemctl start docker'"
sudo systemctl start docker
echo "Docker is now runinng"

# start pycharm and webstorm
echo "starting pycharm"
nohup /home/centralstation/.local/share/JetBrains/Toolbox/scripts/pycharm &

echo "pycharm is now running"

echo "sleeping for 5 seconds"
sleep 10 

echo "starting webstorm"
nohup /home/centralstation/.local/share/JetBrains/Toolbox/scripts/webstorm &
echo "webstorm is now running"


# go into the python directory
echo "moving into the notetaker project directory"
cd /opt/webapps/python/projects/notetaker

# start brave browser
echo "starting Brave Browser"
nohup /usr/bin/brave-browser-stable & 

# start the docker container
echo "building the notetaker project"
notetaker -b

