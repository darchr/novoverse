#!/bin/sh

cd $HOME
git clone https://github.com/takekoputa/simple-vectorizable-microbenchmarks
cd simple-vectorizable-microbenchmarks
git pull
cd permutating_scatter
make -f makefiles/Makefile-hw+sve clean
make -f makefiles/Makefile-hw+sve M5_BUILD_PATH=$HOME/gem5/util/m5/build/arm64/ M5OPS_HEADER_PATH=$HOME/gem5/include/

