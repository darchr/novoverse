#!/bin/bash

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install build-essential git python3-pip gfortran cmake ninja-build git-lfs
pip install scons --user
pip install meson --user
