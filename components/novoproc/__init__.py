from gem5.isas import ISA
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from ._novo_o3_cpu import NovoO3CPU

class NovoCore(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = NovoO3CPU()
        super().__init__(core, ISA.ARM)

class NovoProcessor(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [NovoCore() for _ in range(num_cores)]
        super().__init__(cores)


