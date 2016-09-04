#!/bin/bash

# ------------------------------------------------------------------------------
#
# BOOTER: DISPLAY
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

echo "[DISPLAY] Booting."

# Use getopts to pull the -i param from the commandline, to determine whether
# requirements install is being requested or explicityly denied

while getopts i: opts; do
  case ${opts} in
    i) param_install="${OPTARG}";;

  esac
done

if [[ -n "$param_install" ]]; then
  if [[ "$param_install" = "false" ]]; then
    install_requirements=false

  fi
fi

# If requirements should be installed (yes by default) go forward with the
# install procedure before running.

if $install_requirements; then
  echo "[DISPLAY] Installing system requirements."
  sudo pip install -r requirements.txt > logs/runtime_output.txt 2> logs/runtime_errors.txt

else
  echo "[DISPLAY] Skipping system requirements install."

fi

# Run the service

echo "[DISPLAY] Starting service."

python boot.py
