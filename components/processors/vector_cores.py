from abc import abstractmethod

from m5.objects import BaseISA, System

from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_core import SimpleCore


from .novocore import NovoCore


class BaseVectorParameters:
    def __init__(self, is_fullsystem: bool):
        self.is_fullsystem = is_fullsystem

    def apply_core_change(self, core: SimpleCore):
        self._apply_isa_change(core.isa)
        self._apply_isa_change(core.decoder[0].isa)

    def apply_system_change(self, system_object: System):
        self._apply_system_change(system_object)

    @abstractmethod
    def _apply_isa_change(self, isa_object: BaseISA):
        pass

    @abstractmethod
    def _apply_system_change(self, system_object: System):
        pass


class ARM_SVE_Parameters(BaseVectorParameters):
    def __init__(self, vlen, is_fullsystem: bool):
        super().__init__(is_fullsystem)
        self.vlen = vlen
        # in gem5, the vector register length (vlen) is sve_vl * 128
        assert (vlen % 128 == 0) and (vlen > 0) and (vlen <= 2048)

    @overrides(BaseVectorParameters)
    def _apply_isa_change(self, isa_object: BaseISA):
        if not self.is_fullsystem:
            isa_object[0].sve_vl_se = self.vlen // 128

    @overrides(BaseVectorParameters)
    def _apply_system_change(self, system_object: System):
        if self.is_fullsystem:
            system_object.sve_vl = self.vlen // 128


class RVV_Parameters(BaseVectorParameters):
    def __init__(self, elen, vlen, is_fullsystem: bool):
        super().__init__(is_fullsystem)
        self.elen = elen
        self.vlen = vlen

    @overrides(BaseVectorParameters)
    def _apply_isa_change(self, isa_object: BaseISA):
        isa_object[0].elen = self.elen
        isa_object[0].vlen = self.vlen

    @overrides(BaseVectorParameters)
    def _apply_system_change(self, system_object: System):
        raise NotImplementedError(
            "RVV configuration does not affect system object"
        )


class SimpleVectorCore(SimpleCore):
    def __init__(
        self,
        cpu_type: CPUTypes,
        core_id: int,
        isa: ISA,
        isa_vector_parameters: BaseVectorParameters,
    ):
        super().__init__(cpu_type, core_id, isa)
        isa_vector_parameters.apply_core_change(self.core)


class NovoVectorCore(NovoCore):
    def __init__(
        self,
        core_id: int,
        isa_vector_parameters: BaseVectorParameters,
    ):
        super().__init__()
        self.core.cpu_id = core_id
        isa_vector_parameters.apply_core_change(self.core)
