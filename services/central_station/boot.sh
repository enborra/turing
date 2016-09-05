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


param_install=""
install_requirements=true

# If the install command-line param is null, go ahead with install of all
# requirements.txt dependencies

echo "[CENTRALSTATION] Booting."

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
  npm install

else
  echo "[CENTRALSTATION] Skipping system requirements install."

fi

# Run the service

echo "[CENTRALSTATION] Starting service."

PATH_BIN_NODE="/usr/local/bin/node"
PATH_APP="$HOME/projects/turing"

"$PATH_BIN_NODE" /usr/local/projects/turing/services/central_station/boot.js
