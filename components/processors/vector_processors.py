from m5.util import warn

from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.components.boards.mem_mode import MemMode
from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.processors.cpu_types import CPUTypes, get_mem_mode
from gem5.components.processors.base_cpu_processor import BaseCPUProcessor
from gem5.components.processors.switchable_processor import SwitchableProcessor

from .vector_cores import (
    BaseVectorParameters,
    SimpleVectorCore,
    NovoVectorCore,
)


class SimpleVectorProcessor(BaseCPUProcessor):
    def __init__(
        self,
        cpu_type: CPUTypes,
        num_cores: int,
        isa: ISA,
        isa_vector_parameters: BaseVectorParameters,
    ):
        super().__init__(
            cores=[
                SimpleVectorCore(cpu_type, core_id, isa, isa_vector_parameters)
                for core_id in range(num_cores)
            ]
        )


class SimpleSwitchableVectorProcessor(SwitchableProcessor):
    def __init__(
        self,
        starting_core_type: CPUTypes,
        switch_core_type: CPUTypes,
        num_cores: int,
        isa: ISA,
        isa_vector_parameters: BaseVectorParameters,
    ) -> None:
        if num_cores <= 0:
            raise AssertionError("Number of cores must be a positive integer!")
        self._start_key = "start"
        self._switch_key = "switch"
        self._current_is_start = True
        self._mem_mode = get_mem_mode(starting_core_type)
        switchable_cores = {
            self._start_key: [
                SimpleVectorCore(
                    cpu_type=starting_core_type,
                    core_id=i,
                    isa=isa,
                    isa_vector_parameters=isa_vector_parameters,
                )
                for i in range(num_cores)
            ],
            self._switch_key: [
                SimpleVectorCore(
                    cpu_type=switch_core_type,
                    core_id=i,
                    isa=isa,
                    isa_vector_parameters=isa_vector_parameters,
                )
                for i in range(num_cores)
            ],
        }
        super().__init__(
            switchable_cores=switchable_cores, starting_cores=self._start_key
        )

    @overrides(SwitchableProcessor)
    def incorporate_processor(self, board: AbstractBoard) -> None:
        super().incorporate_processor(board=board)
        if (
            board.get_cache_hierarchy().is_ruby()
            and self._mem_mode == MemMode.ATOMIC
        ):
            warn(
                "Using an atomic core with Ruby will result in "
                "'atomic_noncaching' memory mode. This will skip caching "
                "completely."
            )
            self._mem_mode = MemMode.ATOMIC_NONCACHING
        board.set_mem_mode(self._mem_mode)

    def switch(self):
        """Switches to the "switched out" cores."""
        if self._current_is_start:
            self.switch_to_processor(self._switch_key)
        else:
            self.switch_to_processor(self._start_key)
        self._current_is_start = not self._current_is_start


class SwitchableNovoVectorProcessor(SwitchableProcessor):
    def __init__(
        self,
        starting_core_type: CPUTypes,
        num_cores: int,
        isa: ISA,
        isa_vector_parameters: BaseVectorParameters,
    ):
        if num_cores <= 0:
            raise AssertionError("Number of cores must be a positive integer!")
        self._start_key = "start"
        self._switch_key = "switch"
        self._current_is_start = True
        self._mem_mode = get_mem_mode(starting_core_type)
        switchable_cores = {
            self._start_key: [
                SimpleVectorCore(
                    cpu_type=starting_core_type,
                    core_id=i,
                    isa=isa,
                    isa_vector_parameters=isa_vector_parameters,
                )
                for i in range(num_cores)
            ],
            self._switch_key: [
                NovoVectorCore(
                    core_id=i,
                    isa_vector_parameters=isa_vector_parameters,
                )
                for i in range(num_cores)
            ],
        }
        super().__init__(
            switchable_cores=switchable_cores, starting_cores=self._start_key
        )

    @overrides(SwitchableProcessor)
    def incorporate_processor(self, board: AbstractBoard) -> None:
        super().incorporate_processor(board=board)
        if (
            board.get_cache_hierarchy().is_ruby()
            and self._mem_mode == MemMode.ATOMIC
        ):
            warn(
                "Using an atomic core with Ruby will result in "
                "'atomic_noncaching' memory mode. This will skip caching "
                "completely."
            )
            self._mem_mode = MemMode.ATOMIC_NONCACHING
        board.set_mem_mode(self._mem_mode)

    def switch(self):
        """Switches to the "switched out" cores."""
        if self._current_is_start:
            self.switch_to_processor(self._switch_key)
        else:
            self.switch_to_processor(self._start_key)
        self._current_is_start = not self._current_is_start
