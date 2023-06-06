
from components.novoproc import NovoProcessor
from components.octopi import OctopiCache

from gem5.components.memory.multi_channel import DualChannelDDR4_2400
from gem5.components.boards.simple_board import SimpleBoard

from gem5.resources import Resource

# For now, we are going to use "SimpleBoard" since this will work with SE mode
# easily. However, we will probably want to replace this with "ArmBoard" in the
# future. We could also create our own "NovoBoard" if we need to specialize it.
board = SimpleBoard(
    clk_freq="2GHz",
    processor=NovoProcessor(num_cores=1),
    memory=DualChannelDDR4_2400(),
    cache_hierarchy=OctopiCache(),
)
