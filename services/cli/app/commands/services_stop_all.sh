#!/bin/bash

echo '[TURING] Stopping services.'

sudo systemctl stop centralstation.service
sudo systemctl stop turing.display.service
