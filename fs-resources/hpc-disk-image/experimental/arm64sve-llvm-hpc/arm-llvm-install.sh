#!/bin/bash

if [ ! -f arm-compiler-for-linux_23.04_Ubuntu-22.04_aarch64.tar ]; then
    wget https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_Ubuntu-22.04_aarch64.tar
    tar xf arm-compiler-for-linux_23.04_Ubuntu-22.04_aarch64.tar
    cd arm-compiler-for-linux_23.04_Ubuntu-22.04
    sudo ./arm-compiler-for-linux_23.04_Ubuntu-22.04.sh -a
else
    echo "The file arm-compiler-for-linux_23.04_Ubuntu-22.04_aarch64.tar exists and probably means the arm compilers have been installed."
    echo "If you want to re-install the compiler, please remove the file before running the script again."
fi
