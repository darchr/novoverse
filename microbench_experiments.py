from typing import List

def get_benchmarks() -> List[str]:
    from microbench import workloads

    return list(workloads.keys())

def run_microbench(benchmark: str):
    from components.novoproc import NovoProcessor
    from components.octopi import OctopiCache
    from microbench import workloads

    from gem5.components.boards.simple_board import SimpleBoard
    from gem5.components.memory.multi_channel import DualChannelDDR4_2400
    from gem5.simulate.simulator import Simulator

    # For now, we are going to use "SimpleBoard" since this will work with SE mode
    # easily. However, we will probably want to replace this with "ArmBoard" in the
    # future. We could also create our own "NovoBoard" if we need to specialize it.
    board = SimpleBoard(
        clk_freq="2GHz",
        processor=NovoProcessor(num_cores=1),
        memory=DualChannelDDR4_2400(),
        cache_hierarchy=OctopiCache(
            l1d_size="32kB",
            l1i_size="32kB",
            l2_size="256kB",
            l3_size="4MB",
            l1d_assoc=8,
            l1i_assoc=8,
            l2_assoc=8,
            l3_assoc=16,
            num_core_complexes=1,
            is_fullsystem=False,
        ),
    )

    board.set_workload(workloads[benchmark])

    simulator = Simulator(board)

    simulator.run()