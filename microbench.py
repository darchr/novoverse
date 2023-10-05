import os


def run_microbench(benchmark):
    import m5

    from microbench_vertical import workloads
    from gem5.simulate.simulator import Simulator
    from components.systems import NovoverseSystemSE

    system = NovoverseSystemSE(
        clk_freq="4GHz", num_cores=8, num_channels=4, vlen=256
    )
    system.set_workload(workloads[benchmark])

    with open(os.path.join(m5.options.outdir, "benchmark"), "w") as outfile:
        outfile.writelines([f"Benchmark: {benchmark}"])

    simulator = Simulator(system)
    simulator.run()
