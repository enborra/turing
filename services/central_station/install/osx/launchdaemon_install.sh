#!/bin/bash

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.29.0/install.sh | bash && source ~/.nvm/nvm.sh

nvm install v4.5.0

sudo ln -s /usr/local/turing/services/central_station/system/com.turing.dali.central_station.plist /Library/LaunchDaemons/com.turing.dali.central_station.plist
