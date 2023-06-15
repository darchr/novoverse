#!/bin/bash

# Copyright (c) 2023 The Regents of the University of California.
# SPDX-License-Identifier: BSD 3-Clause

cd $HOME
git clone https://gem5.googlesource.com/public/gem5/
cd $HOME/gem5/util/m5
/home/ubuntu/.local/bin/scons arm64.CROSS_COMPILE= build/arm64/out/m5

mv /home/ubuntu/serial-getty@.service /lib/systemd/system/
mv /home/ubuntu/gem5/util/m5/build/arm64/out/m5 /sbin
ln -s /sbin/m5 /sbin/gem5
mv /home/ubuntu/gem5-init.sh /root/
chmod +x /root/gem5-init.sh
echo "/root/gem5-init.sh" >> /root/.bashrc
