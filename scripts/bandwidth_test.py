import os
import argparse

from math import ceil
from util import novoverse


def generate_traces(num_cores, src_id, dst_id, sharing, addr, size, outdir):
    rd_perc = {"read": 100, "write": 0}

    ret = []
    for i in range(num_cores):
        with open(
            os.path.join(os.path.abspath(outdir), f"core_{i}"), "w"
        ) as trace:
            if i == src_id:
                state_lines = [
                    f"STATE 0 0 LINEAR {rd_perc[sharing]} {addr} {addr + 2097152} {size} 500 500 2097152\n",
                    f"STATE 1 1000000000000 IDLE\n",
                ]
                transition_lines = [
                    "INIT 0\n",
                    "TRANSITION 0 1 1\n",
                    "TRANSITION 1 1 1\n",
                ]
            elif i == dst_id:
                state_lines = [
                    f"STATE 0 1000000000 IDLE\n",
                    f"STATE 1 0 EXIT\n",
                    f"STATE 2 0 LINEAR {rd_perc[sharing]} {addr} {addr + 2097152} {size} 500 500 2097152\n",
                    f"STATE 3 0 EXIT\n",
                    f"STATE 4 100000000 IDLE\n",
                ]
                transition_lines = [
                    "INIT 0\n",
                    "TRANSITION 0 1 1\n",
                    "TRANSITION 1 2 1\n",
                    "TRANSITION 2 3 1\n",
                    "TRANSITION 3 4 1\n",
                    "TRANSITION 4 4 1\n",
                ]
            else:
                state_lines = [f"STATE 0 10000000000000 IDLE\n"]
                transition_lines = ["INIT 0\n", "TRANSITION 0 0 1\n"]
            trace.writelines(state_lines + transition_lines)
            ret.append(trace.name)
    return ret


@novoverse
def run_core_to_core_bandwidth(inputs):
    import m5

    from m5.debug import flags
    from m5.objects import Root, DDR4_2400_8x8

    from gem5.components.boards.test_board import TestBoard
    from gem5.components.memory.memory import ChanneledMemory
    from gem5.components.processors.traffic_generator import TrafficGenerator

    from components.cmn import CoherentMeshNetwork

    src_id, dst_id, sharing, addr, size, debug = inputs
    with open(os.path.join(m5.options.outdir, "params"), "w") as params_file:
        params_file.writelines(
            [
                f"sharing: {sharing}\n",
                f"srd_id: {src_id}\n",
                f"dst_id: {dst_id}\n",
                f"addr: {addr}\n",
                f"size: {size}\n",
            ]
        )

    generator = TrafficGenerator(
        generate_traces(
            8, src_id, dst_id, sharing, addr, size, m5.options.outdir
        )
    )

    memory = ChanneledMemory(DDR4_2400_8x8, 4, 128, size="16GiB")
    cache = CoherentMeshNetwork(slice_interleaving_size="4KiB")
    board = TestBoard(
        clk_freq="4GHz",
        generator=generator,
        cache_hierarchy=cache,
        memory=memory,
    )

    root = Root(full_system=False, system=board)

    board._pre_instantiate()
    cache.set_l2_size("2MiB")

    m5.instantiate()

    generator.start_traffic()
    print("Beginning simulation!")
    exit_events_countered = 0
    while True:
        exit_event = m5.simulate()
        exit_events_countered += 1
        print(
            f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}."
        )
        print(f"Received {exit_events_countered} exit events.")
        if exit_events_countered == 1:
            print(f"Receiver core starting {sharing}.")
            print("Resetting stats.")
            if debug:
                flags["ProtocolTrace"].enable()
                flags["RubyNetwork"].enable()
            m5.stats.reset()
        if exit_events_countered == 2:
            print(f"Receiver core done {sharing} process.")
            if debug:
                flags["ProtocolTrace"].disable()
                flags["RubyNetwork"].disable()
            break
    print("Simulation over.")
    print("Dumping the stats.")


def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_id", type=int, help="Source core number")
    parser.add_argument("dst_id", type=int, help="Destination core number")
    parser.add_argument(
        "sharing",
        type=str,
        help="Whether to measure read sharing latency or write sharing latency.",
        choices=["read", "write"],
    )
    parser.add_argument(
        "addr",
        type=int,
        help="Beginning address of 512KB block to share",
    )
    parser.add_argument("size", type=int, help="Size of each request")
    parser.add_argument(
        "--dprint",
        action="store_const",
        const=True,
        dest="debug",
        default=False,
        help="Wheter to print debug logs.",
    )

    args = parser.parse_args()

    return [
        args.src_id,
        args.dst_id,
        args.sharing,
        args.addr,
        args.size,
        args.debug,
    ]


if __name__ == "__m5_main__":
    run_core_to_core_bandwidth(get_inputs())
