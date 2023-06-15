#!/bin/sh

cd $HOME
git clone https://github.com/takekoputa/NPB
cd NPB
git pull
cd NPB3.4-OMP
make clean
cp $HOME/benchmark-configs/NPB/make.def $HOME/NPB/NPB3.4-OMP/config/make.def
cp $HOME/benchmark-configs/NPB/suite.def $HOME/NPB/NPB3.4-OMP/config/suite.def
mkdir bin
make suite -j `nproc`
