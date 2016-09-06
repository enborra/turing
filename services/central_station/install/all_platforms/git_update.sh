

# Stop existing services with system dependencies

echo '[REPO] Stopping services'
sudo systemctl stop centralstation.service
sudo systemctl stop turing.display.service

# Update from git origin master

echo '[REPO] Pulling new code down from origin master.'
cd $TURING_APP_DIR
git pull origin master
cd /home/pi/projects/turing/services/central_station

# Restart system-dependent services

echo '[REPO] Restarting services.'
sudo systemctl start centralstation.service
sudo systemctl start turing.display.service
