import argparse

import m5
from m5.objects import Root

from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.boards.test_board import TestBoard

from components.saga.cache_hierarchy import SagaCacheHierarchy
from components.strided_generator import StridedGenerator


def get_generator_class(pattern_string):
    translator = {
        "linear": LinearGenerator,
        "strided": StridedGenerator,
        "random": RandomGenerator,
    }
    return translator[pattern_string]


def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "traffic_pattern",
        type=str,
        help="Pattern of traffic to use",
        choices=["linear", "strided", "random"],
    )
    parser.add_argument(
        "demand_rate", type=int, help="Rate of demand bandwidth in GiB/s"
    )
    parser.add_argument(
        "read_percentage",
        type=int,
        help="Percentage of requests that are reads.",
    )

    args = parser.parse_args()
    return args.traffic_pattern, args.demand_rate, args.read_percentage


if __name__ == "__m5_main__":
    pattern, rate, read_percentage = get_inputs()
    memory = DualChannelDDR4_2400()
    generator = get_generator_class(pattern)(
        num_cores=8,
        rate=f"{rate}GiB/s",
        max_addr=memory.get_size(),
        rd_perc=read_percentage,
    )
    board = TestBoard(
        clk_freq="4GHz",
        generator=generator,
        cache_hierarchy=SagaCacheHierarchy(),
        memory=memory,
    )

    root = Root(full_system=False, system=board)

    board._pre_instantiate()
    m5.instantiate()

    generator.start_traffic()
    print("Beginning simulation!")
    exit_event = m5.simulate()
    print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}.")
