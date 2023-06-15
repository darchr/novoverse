#!/bin/bash

cd $HOME
git clone https://github.com/takekoputa/MemoryLatencyTest
cd MemoryLatencyTest
git pull
mkdir build
/home/ubuntu/.local/bin/meson setup build
cd build
ninja -j`nproc`
