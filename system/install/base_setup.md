# Setting up basic environment for app scripts to run


## INSTALL NODE.JS

ONLY INSTALL NODE FROM HERE:
https://github.com/cncjs/cncjs/wiki/Setup-Guide:-Raspberry-Pi-%7C-Install-Node.js-via-Node-Version-Manager-(NVM)


##1. Add environmental variables for turing app path

### OSX: Add the following to ~/.bash_profile so that it sets on every login

#### a. sudo nano ~/.bash_profile
#### b. Add this line to .bash_profile:
  export TURING_APP_DIR=~/etc/turing
####c. source ~/.bash_profile

### Raspberry Pi: Add the following to ~/.bashrc
  export TURING_APP_DIR=/private/etc/turing

## 2. Install Python & Homebrew

### a. Run the following on macOS commandline:
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

### b. Run the following on macOS commandline:
  brew install python3

  (may return an error indicating that a prior version of Python is already installed. If so, disregard and move on).

## 3. Install pip & framework requirements

### a. Download setuptools
  curl -O http://python-distribute.org/distribute_setup.py

### b. Run setuptools install
  python distribute_setup.py

### c. Download pip
  curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py

### d. Install pip
  python get-pip.py

  # download and install setuptools
  curl -O https://bootstrap.pypa.io/ez_setup.py
  python3 ez_setup.py
  # download and install pip
  curl -O https://bootstrap.pypa.io/get-pip.py
  python3 get-pip.py

### e. Install Turing pip requirements defined in requirements.txt
  sudo pip3 install -r requirements.txt

## 4. Run install_env.sh
