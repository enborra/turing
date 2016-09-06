#!/bin/bash


# Stop existing services with system dependencies

sudo sh "$TURING_APP_DIR/services/cli/app/commands/services_stop_all.sh"

# Update from git origin master

echo '[REPO] Pulling new code down from origin master.'
cd $TURING_APP_DIR
git pull origin master
cd /home/pi/projects/turing/services/central_station

# Restart system-dependent services

sudo sh "$TURING_APP_DIR/services/cli/app/commands/services_start_all.sh"
