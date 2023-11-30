from gem5.components.cachehierarchies.abstract_cache_hierarchy import (
    AbstractCacheHierarchy,
)
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)

from gem5.isas import ISA
from gem5.utils.override import overrides
from gem5.components.boards.abstract_board import AbstractBoard

from m5.objects import Cache, L2XBar, BaseXBar, SystemXBar, BadAddr, Port

from .caches import ICache, DCache, L2Cache, L3Cache


class BineCache(AbstractClassicCacheHierarchy):
    @staticmethod
    def _get_default_membus() -> SystemXBar:
        membus = SystemXBar(width=64)
        membus.badaddr_responder = BadAddr()
        membus.default = membus.badaddr_responder.pio
        return membus

    def __init__(
        self, membus: BaseXBar = _get_default_membus.__func__()
    ) -> None:
        AbstractClassicCacheHierarchy.__init__(self=self)
        self.membus = membus

    @overrides(AbstractClassicCacheHierarchy)
    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    @overrides(AbstractClassicCacheHierarchy)
    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    @overrides(AbstractCacheHierarchy)
    def incorporate_cache(self, board: AbstractBoard) -> None:
        # Set up the system port for functional access from the simulator.
        board.connect_system_port(self.membus.cpu_side_ports)

        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports = port

        self.l3bus = L2XBar(width=64)
        self.l3cache = L3Cache(
            cpu_side=self.l3bus.mem_side_ports,
            mem_side=self.membus.cpu_side_ports,
        )
        self.l2buses = [
            L2XBar() for _ in range(board.get_processor().get_num_cores())
        ]
        self.l2caches = [
            L2Cache(
                cpu_side=self.l2buses[i].mem_side_ports,
                mem_side=self.l3bus.cpu_side_ports,
            )
            for i in range(board.get_processor().get_num_cores())
        ]
        self.l1icaches = [
            ICache(mem_side=self.l2buses[i].cpu_side_ports)
            for i in range(board.get_processor().get_num_cores())
        ]
        self.l1dcaches = [
            DCache(mem_side=self.l2buses[i].cpu_side_ports)
            for i in range(board.get_processor().get_num_cores())
        ]

        if board.has_coherent_io():
            self._setup_io_cache(board)

        for i, cpu in enumerate(board.get_processor().get_cores()):
            cpu.connect_icache(self.l1icaches[i].cpu_side)
            cpu.connect_dcache(self.l1dcaches[i].cpu_side)

            cpu.connect_walker_ports(
                self.membus.cpu_side_ports, self.membus.cpu_side_ports
            )

            if board.get_processor().get_isa() == ISA.X86:
                int_req_port = self.membus.mem_side_ports
                int_resp_port = self.membus.cpu_side_ports
                cpu.connect_interrupt(int_req_port, int_resp_port)
            else:
                cpu.connect_interrupt()

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=50,
            data_latency=50,
            response_latency=50,
            mshrs=20,
            size="1kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()
