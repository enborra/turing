# Setting up basic environment for app scripts to run

1. Add environmental variables for turing app path
OSX: Add the following to ~/.bash_profile so that it sets on every login
export TURING_APP_DIR=~/projects/turing

Raspberry Pi: Add the following to ~/.bashrc
export TURING_APP_DIR=/home/pi/projects/turing

2. Install Python & Homebrew
Run the following on macOS commandline:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Run the following on macOS commandline:
brew install python3

3. Install pip & framework requirements
- Install pip
curl -O http://python-distribute.org/distribute_setup.py
python distribute_setup.py
curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

sudo pip3 install -r requirements.txt

4. Run install_env.sh
