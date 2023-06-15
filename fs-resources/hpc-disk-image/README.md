# Packer scripts for building HPC disk images

## Status

|                     | rv64gc | arm64 | arm64sve |
| ------------------- | ------ | ----- | -------- |
| stream              |     ✔ |    ✔ |       ✔ |
| gups                |     ❌ |    ❌ |       ❌ |
| spatter             |     ✔ |    ✔ |       ✔ |
| npb                 |     ✔ \*|    ✔\* |       ✔\* |
| point-chasing       |     ❌ |    ❌ |       ❌ |
| permutating-scatter |     ✔ |    ✔ |       ✔ |
| permutating-gather  |     ✔ |    ✔ |       ✔ |

\*Compiling is.D.x resulted in compilation error.

## Download Packer

See [https://developer.hashicorp.com/packer/downloads](https://developer.hashicorp.com/packer/downloads).

## Building the rv64gc Disk Image

### Downloading the Pre-installed RISC-V Disk Image

We chose this disk image because the disk image is known to work with QEMU.

See [https://ubuntu.com/download/risc-v](https://ubuntu.com/download/risc-v).

```sh
wget https://cdimage.ubuntu.com/releases/22.04.2/release/ubuntu-22.04.2-preinstalled-server-riscv64+unmatched.img.xz
xz -dk ubuntu-22.04.2-preinstalled-server-riscv64+unmatched.img.xz
mv ubuntu-22.04.2-preinstalled-server-riscv64+unmatched.img rv64gc-hpc-2204.img
qemu-img resize rv64gc-hpc-2204.img +20G
```

### Launching a QEMU Instance

```sh
qemu-system-riscv64 -machine virt -nographic \
     -m 16384 -smp 8 \
     -bios /usr/lib/riscv64-linux-gnu/opensbi/generic/fw_jump.elf \
     -kernel /usr/lib/u-boot/qemu-riscv64_smode/uboot.elf \
     -device virtio-net-device,netdev=eth0 \
     -netdev user,id=eth0,hostfwd=tcp::5555-:22 \
     -drive file=rv64gc-hpc-2204.img,format=raw,if=virtio
```

### Changing the Default Password

Upon the first boot, when you try to login to the `ubuntu` account, the OS will ask you to change the password.
The default password is `ubuntu`.
The new password should be `automato`, which is specified in `rv64gc-hpc.json`.

To login to the guest machine,

```sh
ssh -p 5555 ubuntu@localhost
```

### Running the Packer Script for RISC-V

While the QEMU Instance is running,

```sh
./packer build rv64gc-hpc.json
```

## Building the arm64 Disk Image

### Downloading the arm64 Cloud Disk Image

See [https://cloud-images.ubuntu.com/](https://cloud-images.ubuntu.com/).

```sh
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
qemu-img convert jammy-server-cloudimg-arm64.img -O raw ./arm64-hpc-2204.img
qemu-img resize -f raw arm64-hpc-2204.img +20G
```

### Setting up an SSH key pair

The following set of commands generate a pair of private and public ssh keys in
`~/.ssh/id_rsa_arm_disk` and `~/.ssh/id_rsa_arm_disk.pub` respectively.
You can change the path to store this pair by changing the argument passed to
the `-f` flag.
If you do so, make sure that `ssh_certificate_file` in `arm64-hpc.json` and
`arm64sve-hpc.json` correspond to this path.

```sh
ssh-keygen -C "ubuntu@localhost" -f ~/.ssh/id_rsa_arm_disk
```

### Making a Cloud Init Config Image

Typically a cloud image will use `cloud-init` to initialize a cloud instance.
In this case, we will use `cloud-init` to set up an SSH key so that we can login
to the guest QEMU instance.
This is necessary because the downloaded cloud image does not contain any user.
Setting up a cloud init config allows us to create a user on the first boot.

You might not have `cloud-init` installed on your machine.
To install `cloud-init` on your machine, run the following commands.
Please note that the following commands are tested with debian
(specifically ubuntu).

```sh
sudo apt install cloud-init
sudo apt install cloud-image-utils
```

We will create a file called `cloud.txt` to store the cloud init configuration.
Typically the configuration looks like,

```
#cloud-config
users:
  - name: ubuntu
    lock_passwd: false
    groups: sudo
    sudo: ['ALL=(ALL) NOPASSWD:ALL']
    shell: /bin/bash
    ssh-authorized-keys:
      - ssh-rsa AAAAJLKFJEWOIJRNJF... <- insert the public key here (e.g., the content of ~/.ssh/id_rsa_arm_disk.pub)
```

Then, we create a cloud init image that we can input to qemu later,

```sh
cloud-localds --disk-format qcow2 cloud.img cloud.txt
```

Note that this image is of qcow2 format.

### Launching a QEMU Instance

To launch a QEMU instance you have to have QEMU Arm system and its EFI files
installed on your machine.
To install these dependencies, run the following commands (tested on debian).

```sh
sudo apt install qemu-system-arm
sudo apt install qemu-efi-aarch64
```

Now that you have QEMU and the supplementary files installed, run the following
set of commands to launch a qemu instance.

```sh
dd if=/dev/zero of=flash0.img bs=1M count=64
dd if=/usr/share/qemu-efi-aarch64/QEMU_EFI.fd of=flash0.img conv=notrunc
dd if=/dev/zero of=flash1.img bs=1M count=64
qemu-system-aarch64 -m 16384 -smp 8 -cpu cortex-a57 -M virt \
    -nographic -pflash flash0.img -pflash flash1.img \
    -drive if=none,file=arm64-hpc-2204.img,id=hd0 -device virtio-blk-device,drive=hd0 \
    -drive if=none,id=cloud,file=cloud.img -device virtio-blk-device,drive=cloud \
    -netdev user,id=user0 -device virtio-net-device,netdev=eth0 \
    -netdev user,id=eth0,hostfwd=tcp::5555-:22
```

### Running the Packer Script for arm64

While the QEMU Instance is running, open a new shell and run

```sh
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa_arm_disk
./packer build arm64-hpc.json
```

Congrats, your disk image in `arm64-hpc-2204.img` is ready.

**REMINDER**: Make sure to check that `ssh_certificate_file` in
`arm64-hpc.json` matches the path you passed as the argument to `-f` in
[Setting up an SSH key pair](#setting-up-an-ssh-key-pair).

### Running the Packer Script for arm64sve
This is similar to building the arm disk image in
[Running the Packer Script for Arm](#running-the-packer-script-for-arm).
You only need to replace `arm64-hpc.json` with `arm64sve-hpc.json`.
