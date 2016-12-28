#!/bin/bash

# Re-enable and re-start centralstation
sudo systemctl enable centralstation.service
sudo systemctl start centralstation.service
