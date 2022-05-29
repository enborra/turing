# Install NVM
# If NVM isn't installed,   
if which nvm > /dev/null
  then
    # NVM is installed, skip
    echo "[NVM] Already installed, skipping."
  else
    # NVM isn't installed, so install it
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
fi

. ~/.bashrc  # Rerun profile after installing nvm

# Install Node
nvm install 8  # Installs Node v8, (nvm install stable) installs Latest version of node
nvm use 8  # Sets Node to use v8

npm install npm@latest -g


# Add turing environmental location
export TURING_APP_DIR=~/etc/turing
export TURING_APP_DIR=/private/etc/turing

# Reload bash
source ~/.bash_profile
