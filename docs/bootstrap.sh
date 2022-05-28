

#
# DOWNLOAD WITH THIS COMMAND
#
# sudo curl -S -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/enborra/turing/master/docs/bootstrap.sh | bash -s
#

# Update system resources
sudo apt-get update --force-yes -qq
sudo apt-get dist-upgrade --force-yes -qq

# Create file structuremeghancakes

sudo mkdir /etc/turing
sudo mkdir /etc/turing/droids
sudo mkdir /etc/turing/outputs
sudo mkdir /etc/turing/services

# Write an example config.json

echo "{\"current-droid\":\"oswald\",\"droid-path\":\"/etc/turing/droids\",\"service-path\":\"/etc/turing/services\"}" > /etc/turing/config.json

# Clone the Turing repo (this repo) to the local system at the /etc location

sudo git clone https://github.com/enborra/turing.git /etc/turing/framework

# Run the install script for the main Turing repo (this repo)

bash /etc/turing/framework/system/install/basics.sh
bash /etc/turing/framework/system/install/install_env.sh
