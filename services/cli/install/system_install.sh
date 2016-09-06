#!/bin/bash

# ------------------------------------------------------------------------------
#
# SERVICE INSTALLER: Turing CLI
#
# This service installer configures the daemon service required to run
# Turing CLI on a Raspberry Pi. This script will not function properly
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


SYSTEM_TYPE_UNKNOWN="unknown"
SYSTEM_TYPE_MAC="mac"
SYSTEM_TYPE_LINUX="linux"

CURR_SYSTEM_TYPE="$SYSTEM_TYPE_UNKNOWN"

# Determine current system type

echo "[INSTALLER] Detecting system."

if [ "$OSTYPE" = "linux"* ]; then
  CURR_SYSTEM_TYPE=$SYSTEM_TYPE_LINUX
  sudo apt-get update;

elif [ "$OSTYPE" = "darwin"* ]; then
  CURR_SYSTEM_TYPE=$SYSTEM_TYPE_MAC

fi

if [ "$CURR_SYSTEM_TYPE" = "$SYSTEM_TYPE_MAC" ]; then
  echo "[INSTALLER] --Current operating system: macOS"
fi

if [ "$CURR_SYSTEM_TYPE" = "$SYSTEM_TYPE_LINUX" ]; then
  echo "[INSTALLER] --Current operating system: Linux"
fi


# Set paths for use

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATH_APP="$TURING_APP_DIR/services/cli/app"

PATH_BIN="/usr/local/bin"
PATH_BIN_CLI_ALIAS="$PATH_BIN/turing"

PATH_APP_CLI="$PATH_APP/cli.py"

# If a file exists at the intended cli alias location,
# remove that file and re-create the alias needed for
# operation.

DOES_ALIAS_REQUIRE_CREATION=false

echo "[INSTALLER] Creating symlink at $PATH_BIN_CLI_ALIAS"

# Set CLI alias and access permissions for script

sudo ln -sf "$PATH_APP_CLI" "$PATH_BIN_CLI_ALIAS"
chmod +x "$PATH_BIN_CLI_ALIAS"

echo '[INSTALLER] Successfully installed Turing CLI.'
