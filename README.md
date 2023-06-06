# Novoverse model

The Novoverse model in gem5 is a set of tuned parameters which models the [Arm Neoverse](https://www.arm.com/products/silicon-ip-cpu/neoverse/neoverse-v1) processors.

## Working with this repository

To checkout (with all submodules) use:

```sh
git clone --recurse-submodules https://github.com/darchr/novoverse
```

If you checked out this repo without `--recurse-submodules` then you can run the following to sync the `gem5/` directory.

```sh
git submodule update --init
```

When needed (e.g., when gem5 version 23.0 is released), to update the submodule, run the following command.

```sh
git submodule update --remote gem5
```

## To do

[ ] Get microbenchmarks into this repository. We probably want to have this as another submodule.
