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

The same commands will work for the microbench directory as it's updated as well.

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

To run a workload, use the `run.py` script.
It takes one parameter, which is the workload name.
Note that you have to use the `MESI_Three_Level` binary to use the Octopi cache and the `CHI` binary to use the Saga or Novocache.
As mentioned above, you may want to use `gem5.fast` instead of `gem5.opt`.

```sh
gem5/build/ALL_MESI_Three_Level/gem5.opt run.py <workload>
```

To see details and modify the system that this run script is simulating, see `microbench_experiements.py`.
This file has a function `run_microbench(benchmark: str)` that runs the microbenchmark specified on the board that is in the function.
The reason that we have a function in a separate file is to support running multiple experiments in parallel (which will come later).

Note that I am going to extend this to run experiments in parallel later.

## Modifying the board

To modify the board that is used in the experiments, modify the `board` variable in the `run_microbench` function in `microbench_experiments.py`.
This file (`microbench_experiments.py`) is where you should change *which* cache hierarchy or core the board is using.

If you want to change the parameters for the processor core or the parameters of the cache hierarchy, then you should modify the files in the `components` directory.
E.g., to specialize the out-of-order core, modify the file `components/novoproc/_novo_o3_cpu.py`.

### The components directory map

- `components/novoproc`
  - This is the main directory for all of the details of the processor that is modeling the N1.
  - `__init__.py`
    - This file contains the wrapper to convert the gem5 O3CPU into the standard library Processor. For single core experiments, this file should not be modified. To extend to multicore, we will need to modify this file to understand groups of cores.
  - `_novo_o3_cpu.py`
    - This file contains the specialized parameters for the N1's out-of-order CPU model. This file *should* be modified with details from the N1 design and based on microbenchmark results.
- `components/octopi`
  - This directory contains the octopi cache hierarchy.
  - This directory will be removed when this is merged into gem5.
- `components/novocache`
  - This directory *will* contain the cache model that is meant to represent the Ampere Altra design.

## Adding workload/microbenchmarks

The `microbench` directory is a submodule with the changes to the microbenchmarks found in prior work.
This directory needs some work to the `Makefile`s and other parts of it to build and deploy the microbenchmarks.

Once a microbenchmark is built (which we should provide details on how to do this in the README here!), then you should add it to the list of microbenchmarks.
See the `workloads` dictionary in `microbench/__init__.py`.

## To do

- [ ] Add the rest of the microbenchmarks.
