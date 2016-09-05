#!/bin/bash


# Install systemd service on an OSX machine

SCRIPT_ORIGIN=$TURING_APP_DIR/services/central_station/system/com.turing.dali.central_station.plist
SCRIPT_LAUNCHD_LOCATION=/Library/LaunchDaemons/com.turing.dali.central_station.plist

# Stop any pre-existing service and disable

echo '[INSTALLER] Stopping any existing running services.'
sudo launchctl unload $SCRIPT_LAUNCHD_LOCATION

# Force-create symlink in LaunchDaemons directory

echo '[INSTALLER] Creating new symlink for service'
sudo ln -sf $SCRIPT_ORIGIN $SCRIPT_LAUNCHD_LOCATION

sudo chmod +x $SCRIPT_LAUNCHD_LOCATION

# Re-load new daemon script

echo '[INSTALLER] Starting new service.'
sudo launchctl load $SCRIPT_LAUNCHD_LOCATION

echo '[INSTALLER] Successfully installed service.'
