from gem5.utils.multiprocessing import Pool

from microbench import run_microbench

workload_names = [
    "CCa",
    "CCe",
    "CCh",
    "CCh_st",
    "CCl",
    "CCm",
    # "CF1",
    "CRd",
    "CRf",
    # "CRm",
    "CS1",
    "CS3",
    "DP1d",
    "DP1f",
    "DPcvt",
    "DPT",
    "DPTd",
    "ED1",
    "EF",
    "EI",
    "EM1",
    "EM5",
    "MC",
    "MCS",
    "MD",
    "M_Dyn",
    "MI",
    "MIM",
    "MIM2",
    "MIP",
    # "ML2",
    "ML2_BW_ld",
    "ML2_BW_ldst",
    "ML2_BW_st",
    # "ML2_st",
    # "MM",
    # "MM_st",
    "STL2",
    # "STL2b",
]

if __name__ == "__m5_main__" or __name__ == "__main__":
    with Pool(processes=4, maxtasksperchild=1) as pool:
        pool.map(run_microbench, workload_names)
