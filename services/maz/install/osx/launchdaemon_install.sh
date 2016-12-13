#!/bin/bash

# ------------------------------------------------------------------------------
#
# SERVICE INSTALLER: Maz
#
# This service installer configures the daemon service required to run
# Central Station on an OSX machine. This script will not function properly
# on a Raspberry Pi system.
#
# The script can be run from any location, and performs the following steps:
#
#   - Disables all existing (running) system daemons with the same name
#
#   - Creates a symlink from the local service plist to /Library/LaunchDaemons,
#     and changes permissions needed for system processes to access the symlink
#
#   - Re-enables and re-starts the newly installed service
#
# ------------------------------------------------------------------------------


# Install systemd service on an OSX machine

SCRIPT_ORIGIN=$TURING_APP_DIR/services/maz/system/com.turing.maz.plist
SCRIPT_LAUNCHD_LOCATION=/Library/LaunchDaemons/com.turing.maz.plist

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
