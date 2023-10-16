import argparse

from util import novoverse


@novoverse
def run_novoverse_fs(inputs):
    import m5

    from gem5.simulate.simulator import Simulator
    from gem5.simulate.exit_event import ExitEvent
    from gem5.resources.resource import Resource, CustomDiskImageResource

    from components.systems import NovoverseSystemFS

    def handle_work_begin():
        print(f"Exit due to m5_work_begin()")
        print(f"info: Resetting stats")
        m5.stats.reset()
        print(f"info: Switching CPU")
        board.get_processor().switch()
        yield False

    def handle_work_end():
        print(f"Exit due to m5_work_end()")
        print(f"info: Dumping stats")
        m5.stats.dump()
        yield False

    def handle_exit():
        print(f"Exit due to m5_exit()")
        yield True

    num_cores, num_channels, vlen, command = inputs
    board = NovoverseSystemFS("4GHz", num_cores, num_channels, vlen)
    # Set the Full System workload.
    board.set_kernel_disk_workload(
        kernel=Resource("arm64-linux-kernel-5.10.110"),
        disk_image=CustomDiskImageResource("arm64sve-hpc.img"),
        bootloader=Resource("arm64-bootloader-foundation"),
        readfile_contents=f"{command}",
    )

    simulator = Simulator(
        board=board,
        on_exit_event={
            ExitEvent.WORKBEGIN: handle_work_begin(),  # save checkpoint here
            ExitEvent.WORKEND: handle_work_end(),
            ExitEvent.EXIT: handle_exit(),
        },
    )
    print("Beginning simulation!")
    simulator.run()


def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-cores", type=int, help="Number of cores", required=True
    )

    parser.add_argument(
        "--num-channels",
        type=int,
        help="Number of memory channels",
        required=True,
    )
    parser.add_argument("--vlen", type=int, help="SVE length", required=True)
    parser.add_argument(
        "--command",
        type=str,
        help="Command inputted to the guest system",
        required=True,
    )
    args = parser.parse_args()

    return [args.num_cores, args.num_channels, args.vlen, args.command]


if __name__ == "__m5_main__":
    run_novoverse_fs(get_inputs())
