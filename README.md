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

## Building gem5

After checking out the gem5 directory (See [above](#working-with-this-repository)), you need to build two versions of gem5, one with the `MESI_Three_Level` protocol to work with the Octopi cache and one with CHI to work with the Saga cache or the Novocache.

```sh
cd gem5
scons build/ALL_MESI_Three_Level/gem5.opt -j `nproc` --default=ALL PROTOCOL=MESI_Three_Level
scons build/ALL_CHI/gem5.opt -j `nproc` --default=ALL PROTOCOL=CHI
```

Note: If you're not making changes to gem5, you may want to build `gem5.fast` instead of `gem5.opt`.
There is a significant performance improvement.

## Running a workload

To run a workload, use the `run_microbenchmark.py` script.
Note that you have to use the `MESI_Three_Level` binary to use the Octopi cache and the `CHI` binary to use the Saga or Novocache.
As mentioned above, you may want to use `gem5.fast` instead of `gem5.opt`.

```sh
gem5/build/ALL_MESI_Three_Level/gem5.opt run_microbenchmark.py
```

## To do

- [ ] Add a parameter to `run_microbenchmark.py` to select the microbenchmark.