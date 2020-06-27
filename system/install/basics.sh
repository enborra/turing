# Install NVM
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
source ~/.bashrc  # Rerun profile after installing nvm

# Install Node
nvm install 8  # Installs Node v8, (nvm install stable) installs Latest version of node
nvm use 8  # Sets Node to use v8

npm install npm@latest -g


# Add turing environmental location
export TURING_APP_DIR=~/etc/turing
source ~/.bash_profile
export TURING_APP_DIR=/private/etc/turing

