#!/bin/sh

cd $HOME
git clone simple-vectorizable-microbenchmarks
cd simple-vectorizable-microbenchmarks/
git pull
git clone https://github.com/nlohmann/json
cd json
git checkout v3.11.2
cd ../spatter
make -f Makefile-hw clean
make -f Makefile-hw M5_BUILD_PATH=$HOME/gem5/util/m5/build/arm64/ M5OPS_HEADER_PATH=$HOME/gem5/include/

cd $HOME
git clone https://github.com/takekoputa/lanl-spatter
cd lanl-spatter
git lfs pull
tar -xzf patterns/flag/static_2d/001.json.tar.gz
tar -xzf patterns/flag/static_2d/001.nonfp.json.tar.gz
tar -xzf patterns/flag/static_2d/001.fp.json.tar.gz
tar -xzf patterns/xrage/asteroid/spatter.json.tar.gz
mv spatter.json patterns/xrage/asteroid/spatter.json
