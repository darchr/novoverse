#!/bin/bash

cd $HOME
git clone https://github.com/takekoputa/MemoryLatencyTest
cd MemoryLatencyTest
git pull
rm -rf build
mkdir build
cd build
/home/ubuntu/.local/bin/meson .. -Dgem5_include_dir=/home/ubuntu/gem5/include -Dm5_build_path=/home/ubuntu/gem5/util/m5/build/arm64/out/
ninja -j`nproc`
