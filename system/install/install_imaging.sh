#!/bin/bash

# OSX:
# Ensure X-Code is installed


# Reference blog post:
# http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/



CAN_INSTALL_PROCEED=true


echo ""
echo "---------------------------------------------------"
echo "ENSURING INSTALLED & UPDATED HOMEBREW"


if [[ $(which brew) == "brew not found" ]]; then
  echo "--Homebrew appears to not be installed."

  # Homebrew needs to be installed
  cd ~
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

else
  echo "--Homebrew is installed."
fi

# Ensure brew updated to latest version

echo "--Updating Homebrew..."

brew update

echo "--Homebrew updated."



# Ensure python installed

if [[ $(which python) == "python not found" ]]; then
  echo "--Python appears not to be installed."
else
  PYTHON_VERSION="$(python -V 2>&1 >/dev/null)"

  if [[ ${PYTHON_VERSION:0:10} == "Python 2.7" ]]; then
    echo "--Running version of Python ($PYTHON_VERSION) compatible with Python 2.7.*"
  else
    echo "--Not running compatible version of Python ($PYTHON_VERSION). Can't continue install."

    CAN_INSTALL_PROCEED=false
  fi
fi

echo ""
echo "---------------------------------------------------"
echo "INSTALLING BREW DEPENDENCIES"


if [[ $CAN_INSTALL_PROCEED == true ]]; then
  echo "--Proceeding with install..."

  # Export Homebrew on bash path - add to ~/.bash_profile
  # not sure this is needed:
  # export PATH=/usr/local/bin:$PATH

  # Reload bash profile
  source ~/.bash_profile

  # Upgrade pip
  sudo -H pip install --upgrade pip

  # Install numpy
  pip install numpy

  # Brew install base toolchain
  brew install cmake
  brew install pkg-config
  brew install jpeg
  brew install libpng
  brew install libtiff
  brew install openexr
  brew install eigen
  brew install tbb

else
  echo "--Cannot proceed with install."
fi



echo ""
echo "---------------------------------------------------"
echo "INSTALLING OPENCV"


if [[ $CAN_INSTALL_PROCEED == true ]]; then
  DIR_PYTHON_SITEPACKAGES="/Library/Python/2.7/site-packages"
  DIR_PYTHON_LIB="/usr/bin/python"
  DIR_PYTHON_INCLUDES="/System/Library/Frameworks/Python.framework/Versions/2.7/include/python2.7"

  IS_CV_INSTALLED=false

  if [ -e "$DIR_PYTHON_SITEPACKAGES/cv2.so" ]; then
    echo "--OpenCV is installed and linked to root Python2.7 install."

    IS_CV_INSTALLED=true
  fi

  if [[ $IS_CV_INSTALLED == false ]]; then
    echo "--Installing OpenCV..."

    cd ~

    # Install OpenCV
    git clone https://github.com/Itseez/opencv.git

    cd ~/opencv
    git checkout 3.0.0

    cd ~
    git clone https://github.com/Itseez/opencv_contrib
    cd opencv_contrib
    git checkout 3.0.0

    cd ~/opencv
    mkdir build
    cd build


    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
    	-D PYTHON2_PACKAGES_PATH="$DIR_PYTHON_SITEPACKAGES" \
    	-D PYTHON2_LIBRARY="$DIR_PYTHON_LIB" \
    	-D PYTHON2_INCLUDE_DIR="$DIR_PYTHON_INCLUDES" \
    	-D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
    	-D BUILD_EXAMPLES=ON \
    	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..

    make
    sudo make install

    echo "--OpenCV successfully installed."
  fi

fi
