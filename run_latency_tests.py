from gem5.utils.multiprocessing import Pool

from latency_test import run_core_to_core_latency

if __name__ == "__m5_main__" or __name__ == "__main__":
    inputs = [
        [sharing, src_id, dst_id, addr, size]
        for src_id in range(8)
        for dst_id in range(8)
        if src_id != dst_id
        for sharing in ["read", "write"]
        for addr in [0, 4096]
        for size in [8, 64]
    ]
    with Pool(processes=4, maxtasksperchild=1) as pool:
        pool.map(run_core_to_core_latency, inputs)
