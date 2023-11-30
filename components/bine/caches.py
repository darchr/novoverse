from m5.objects import Cache, StridePrefetcher


# all copied from binebrank
class ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 16
    size = "64kB"  # (1)
    assoc = 4  # (1)
    writeback_clean = False
    prefetcher = StridePrefetcher(degree=1)


class DCache(Cache):
    tag_latency = 3
    data_latency = 3
    response_latency = 1
    tgts_per_mshr = 16
    writeback_clean = False
    size = "64kB"  # (1)
    mshrs = 20  # (1)
    assoc = 4  # (1)
    # prefetcher = StridePrefetcher(degree=16, latency = 1)


class L2Cache(Cache):
    tag_latency = 5
    data_latency = 5
    response_latency = 2
    mshrs = 46  # (1)
    tgts_per_mshr = 16
    clusivity = "mostly_incl"  # (1)
    assoc = 8  # (1)
    size = "1MB"  # Graviton2
    writeback_clean = True
    # do this in cache config prefetcher = TaggedPrefetcher(degree=16, latency = 1, queue_size = 16)


class L3Cache(Cache):
    tag_latency = 48
    data_latency = 48
    response_latency = 16
    assoc = 16  # (1)
    size = "8MB"  # 1MB per core-duplex but we set this higher due to shared L3 and interconnect
    # do this in cache config prefetcher = TaggedPrefetcher(degree=16, latency = 1, queue_size = 16)
    clusivity = "mostly_excl"
    mshrs = 128
    tgts_per_mshr = 64
    write_buffers = 64
