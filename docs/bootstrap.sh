

#
# DOWNLOAD WITH THIS COMMAND
#
# sudo curl -S -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/enborra/turing/master/docs/bootstrap.sh | bash -s
#

# Run this file remote to kick off install

# Check for git on system
## Install if git doesn't exist

# Check for python on system
## Install if python doesn't exist

# Check for nodejs on system
## Install if nodejs doesn't exist

# Create file structuremeghancakes

sudo mkdir /etc/turing
sudo mkdir /etc/turing/droids
sudo mkdir /etc/turing/outputs
sudo mkdir /etc/turing/services

# Clone the Turing repo (this repo) to the local system at the /etc location

sudo git clone https://github.com/enborra/turing.git /etc/turing/framework

# Run the install script for the main Turing repo (this repo)
