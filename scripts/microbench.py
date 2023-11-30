import os
import argparse

from util import novoverse


@novoverse
def run_microbench(inputs):
    import m5

    from microbenchmarks import workloads_v1
    from gem5.simulate.simulator import Simulator
    from components.systems import NovoverseSystemSE

    benchmark = inputs[0]

    system = NovoverseSystemSE(
        clk_freq="2GHz",
        num_cores=8,
        num_channels=4,
        vlen=256,
    )
    system.set_workload(workloads_v1[benchmark])

    with open(os.path.join(m5.options.outdir, "benchmark"), "w") as outfile:
        outfile.writelines([f"Benchmark: {benchmark}"])

    simulator = Simulator(system)
    simulator.run()


def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "benchmark",
        type=str,
        help="Name of benchmark to run",
    )
    args = parser.parse_args()
    return [args.benchmark]


if __name__ == "__m5_main__":
    run_microbench(get_inputs())
