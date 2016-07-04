#!/bin/sh

if pgrep "boot" > /dev/null
then
    echo "[TURING.BOOT] Initializing..."

    cd /home/pi/projects/turing/os
    sudo python boot.py
    cd /

else
    echo "[TURING] Already running."
