#!/bin/bash

echo '[TURING] Starting services.'

sudo systemctl start centralstation.service
sudo systemctl start turing.display.service
