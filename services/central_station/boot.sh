#!/bin/bash

# ------------------------------------------------------------------------------
#
# BOOTER: CENTRAL STATION
#
# USAGE:
#     Force dependencies install: sh boot.sh -i true
#     Skip dependencies install:  sh boot.sh -i false
#
# ------------------------------------------------------------------------------


PATH_BIN_NPM="/usr/local/bin/npm"
PATH_BIN_NODE="/usr/local/bin/node"

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATH_APP="$CURRENT_DIR/app"

param_install=""
install_requirements=false

# If the install command-line param is null, go ahead with install of all
# requirements.txt dependencies

echo "[CENTRALSTATION] Booting."
cd "$PATH_APP"

# Use getopts to pull the -i param from the commandline, to determine whether
# requirements install is being requested or explicityly denied

while getopts i: opts; do
  case ${opts} in
    i) param_install="${OPTARG}";;

  esac
done

if [ -n "$param_install" ]; then
  if [ "$param_install" = "false" ]; then
    install_requirements=false

  fi
fi

# If requirements should be installed (yes by default) go forward with the
# install procedure before running.

if $install_requirements; then
  echo "[CENTRALSTATION] Installing system requirements."
  $PATH_BIN_NPM install

else
  echo "[CENTRALSTATION] Skipping system requirements install."

fi

# Run the service

echo "[CENTRALSTATION] Starting service."

$PATH_BIN_NODE -v
$PATH_BIN_NPM -v

sudo $PATH_BIN_NPM start
