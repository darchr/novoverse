from gem5.isas import ISA
from gem5.utils.requires import requires
from gem5.components.processors.base_cpu_core import BaseCPUCore

from ._novo_o3_cpu import NovoO3CPU


class NovoCore(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """

    def __init__(self):
        """ """
        requires(ISA.ARM)
        core = NovoO3CPU()
        super().__init__(core, ISA.ARM)
