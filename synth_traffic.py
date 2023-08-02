import argparse

import m5
from m5.objects import Root

from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.boards.test_board import TestBoard

from components.saga.cache_hierarchy import SagaCacheHierarchy

from gem5.components.cachehierarchies.classic.no_cache import NoCache

from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.components.processors.strided_generator import StridedGenerator


def get_generator(
    generator_class, num_cores, min_addr, max_addr, read_percentage
):
    if generator_class == "linear":
        return LinearGenerator(
            num_cores=num_cores,
            rate="40GiB/s",
            min_addr=min_addr,
            max_addr=max_addr,
            block_size=64,
            rd_perc=read_percentage,
        )
    elif generator_class == "random":
        return RandomGenerator(
            num_cores=num_cores,
            rate="40GiB/s",
            min_addr=min_addr,
            max_addr=max_addr,
            block_size=64,
            rd_perc=read_percentage,
        )
    elif generator_class == "strided":
        return StridedGenerator(
            num_cores=num_cores,
            rate="40GiB/s",
            min_addr=min_addr,
            max_addr=max_addr,
            block_size=64,
            subblock_size=64,
            stride_size=num_cores * 64,
            rd_perc=read_percentage,
        )


def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "traffic_pattern",
        type=str,
        help="Pattern of traffic to use",
        choices=["linear", "strided", "random"],
    )
    parser.add_argument(
        "read_percentage",
        type=int,
        help="Percentage of requests that are reads.",
    )

    args = parser.parse_args()
    return args.traffic_pattern, args.read_percentage


if __name__ == "__m5_main__":
    pattern, read_percentage = get_inputs()
    memory = DualChannelDDR4_2400()
    generator = get_generator(
        generator_class=pattern,
        num_cores=8,
        min_addr=0,
        max_addr=memory.get_size(),
        read_percentage=read_percentage,
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
