from gem5.isas import ISA
from gem5.components.processors.base_cpu_core import BaseCPUCore
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor

from ._grace_o3_cpu import GraceO3CPU
from ._grace_pipelined import GracePipelined
from ._grace_12w import Grace12Width
from ._grace_4w import Grace4Width
from ._grace_inf import GraceInf

class GraceCore(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = GraceO3CPU()
        super().__init__(core, ISA.ARM)

class GraceProcessor(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [GraceCore() for _ in range(num_cores)]
        super().__init__(cores)

class GraceCorePipelined(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = GracePipelined()
        super().__init__(core, ISA.ARM)

class GraceProcessorPipelined(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [GraceCorePipelined() for _ in range(num_cores)]
        super().__init__(cores)


class GraceCore12Width(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = Grace12Width()
        super().__init__(core, ISA.ARM)

class GraceProcessor12W(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [GraceCore12Width() for _ in range(num_cores)]
        super().__init__(cores)


class GraceCore4Width(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = Grace4Width()
        super().__init__(core, ISA.ARM)

class GraceProcessor4W(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [GraceCore4Width() for _ in range(num_cores)]
        super().__init__(cores)

class GraceCoreInf(BaseCPUCore):
    """One core of a NovoProcessor. This is modeled after the Arm Neoverse-N1
    core.

    This is an Arm-based model.
    """
    def __init__(self):
        """
        """
        core = GraceInf()
        super().__init__(core, ISA.ARM)

class GraceProcessorInf(BaseCPUProcessor):
    """
    A processor that is composed of a number of NovoCores.

    :param num_cores: The number of cores in the processor.
    """
    def __init__(self, num_cores):
        cores = [GraceCoreInf() for _ in range(num_cores)]
        super().__init__(cores)