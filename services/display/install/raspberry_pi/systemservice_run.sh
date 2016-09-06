#!/bin/bash

# Re-enable and re-start Turing Display
sudo systemctl enable turing.display.service
sudo systemctl start turing.display.service
