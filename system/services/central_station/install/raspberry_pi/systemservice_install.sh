#!/bin/bash

# ------------------------------------------------------------------------------
#
# SERVICE INSTALLER: Central Station
#
# This service installer configures the daemon service required to run
# Central Station on a Raspberry Pi. This script will not function properly
# on an OSX system.
#
# The script can be run from any location, and performs the following steps:
#
#   - Disables all existing (running) system daemons with the same name
#
#   - Copies the local version of the .service file definition into
#     /lib/systemd/system, because systemd doesn't properly support symlinks
#
#   - Re-enables and re-starts the newly installed service
#
# ------------------------------------------------------------------------------


# Install systemd service on a Raspberry Pi machine

SCRIPT_ORIGIN=$TURING_APP_DIR/services/central_station/system/centralstation.service
SCRIPT_SYSTEMD_LOCATION=/lib/systemd/system/centralstation.service

# Stop any pre-existing service and disable

echo '[INSTALLER] Shutting down and disabling any existing services.'
sudo systemctl stop centralstation.service
sudo systemctl disable centralstation.service

# Force-copy of script into systemd directory, and update permissions

echo '[INSTALLER] Copying service definition into systemd.'

sudo cp -f $SCRIPT_ORIGIN $SCRIPT_SYSTEMD_LOCATION
sudo chmod +x $SCRIPT_SYSTEMD_LOCATION

# Reload daemon system

echo '[INSTALLER] Reloading system daemon'
sudo systemctl daemon-reload

# Enable and start new service

echo '[INSTALLER] Starting new service.'
sudo systemctl enable centralstation.service
sudo systemctl start centralstation.service

echo '[INSTALLER] Successfully installed Central Station service.'
