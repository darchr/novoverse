
from m5.objects import (
    ArmO3CPU,
    FUDesc,
    OpDesc,
    FUPool,
)

from m5.objects.FUPool import *

from m5.objects.BranchPredictor import (
    TournamentBP,
    BiModeBP,
)


class O3_ARM_Neoverse_N1_FP(FUDesc):
    """
    This class refers to FP/ASIMD 0/1 (symbol V in (2) table 3)
    Copied from Neoverse V1 optimization guide,
    latency taken for specific instruction in brackets
    """
    # ASIMD arithmetic basis (add & sub)
    opList = [ OpDesc(opClass='SimdAdd', opLat=2),
              # ASIMD absolute diff accum (vaba)
               OpDesc(opClass='SimdAddAcc', opLat=4),
               # ASIMD logical (and)
               OpDesc(opClass='SimdAlu', opLat=2),
               # ASIMD compare (cmeq)
               OpDesc(opClass='SimdCmp', opLat=2),
               # ASIMD FP convert to floating point 64b (scvtf)
               OpDesc(opClass='SimdCvt', opLat=3),
                #ASIMD move, immed (vmov)
               OpDesc(opClass='SimdMisc', opLat=2),
               # ASIMD integer multiply D-form (mul)
               OpDesc(opClass='SimdMult',opLat=4),
               # ASIMD multiply accumulate, D-form (mla)
               OpDesc(opClass='SimdMultAcc',opLat=4),
               #ASIMD shift by immed, (shl)
               OpDesc(opClass='SimdShift',opLat=2),
               # ASIMD shift accumulate (vsra)
               OpDesc(opClass='SimdShiftAcc', opLat=4),
               # ASIMD reciprocal estimate (vrsqrte)
               OpDesc(opClass='SimdSqrt', opLat=9),
                # ASIMD floating point arithmetic (vadd)
               OpDesc(opClass='SimdFloatAdd',opLat=2),
               # ASIMD floating point absolute value (vabs)
               OpDesc(opClass='SimdFloatAlu',opLat=2),
               # ASIMD floating point comapre (fcmgt)
               OpDesc(opClass='SimdFloatCmp', opLat=2),
               # Aarch64 FP convert (fvctas)
               OpDesc(opClass='SimdFloatCvt', opLat=3),
               # ASIMD floating point divide f64 (fdiv)
               OpDesc(opClass='SimdFloatDiv', opLat=11, pipelined=False),
               # Bunch of relatively non-important insts (vneg)
               OpDesc(opClass='SimdFloatMisc', opLat=2),
               # ASIMD floating point multiply (vmul)
               OpDesc(opClass='SimdFloatMult', opLat=4),
               # ASIMD floating point multiply accumulate (vmla)
               OpDesc(opClass='SimdFloatMultAcc',opLat=4),
               # ASIMD floating point square root f64 (vsqrt)
               OpDesc(opClass='SimdFloatSqrt', opLat=12, pipelined=False),
               # SVE reduction, arithmetic, S form (saddv)
               OpDesc(opClass='SimdReduceAdd', opLat=4),
               # SVE reduction, logical (andv)
               OpDesc(opClass='SimdReduceAlu', opLat=6),
               # SVE reduction, arithmetic, S form (smaxv)
               OpDesc(opClass='SimdReduceCmp', opLat=5),
               #SVE floating point associative add (fadda)
               OpDesc(opClass='SimdFloatReduceAdd', opLat=4, pipelined=False),
               # SVE floating point reduction f64 (fmaxv)
               OpDesc(opClass='SimdFloatReduceCmp', opLat=5),
               # Aarch64 FP arithmetic (fadd)
               OpDesc(opClass='FloatAdd', opLat=2),
               # Aarch64 FP compare (fccmpe)
               OpDesc(opClass='FloatCmp', opLat=2),
               # Aarch64 Fp convert (vcvt)
               OpDesc(opClass='FloatCvt', opLat=3),
                # Aarch64 Fp divide (vdiv) // average latency
               OpDesc(opClass='FloatDiv', opLat=11, pipelined=False),
               # Aarch64 Fp square root D-form (fsqrt) // average
               OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False),
               # Aarch64 Fp multiply accumulate (vfma)
               OpDesc(opClass='FloatMultAcc', opLat=4),
               # Aarch64 miscellaneous
               OpDesc(opClass='FloatMisc', opLat=3),
               # Aarch64 Fp multiply (fmul)
               OpDesc(opClass='FloatMult', opLat=3)
               ]

    count = 2


class O3_ARM_Neoverse_N1_Simple_Int(FUDesc):
    """
    This class refers to pipelines Branch0, Integer single Cycles 0,
    Integer single Cycle 1 (symbol B and S in (2) table 3)
    """
    # Aarch64 ALU (Unfortunately branches are put together with IntALU)
    opList = [ OpDesc(opClass='IntAlu', opLat=1) ]
    count = 3

class O3_ARM_Neoverse_N1_Complex_Int(FUDesc):
    """
    This class refers to pipelines integer single/multicycle 1
    (this refers to pipeline symbol M in (2) table 3)
    """
    # Aarch64 Int ALU
    opList = [ OpDesc(opClass='IntAlu', opLat=1),
                # Aarch64 Int mult
                OpDesc(opClass='IntMult', opLat=2),
                # Aarch64 Int divide W-form (sdiv) // we take average
                OpDesc(opClass='IntDiv', opLat=5, pipelined=False),
                # Aarch64 Prefetch
                OpDesc(opClass='IprAccess', opLat=1)
                ]
    count = 1

class O3_ARM_Neoverse_N1_LoadStore(FUDesc):
    """
    This class refers to Load/Store0/1
    (symbol L in Neoverse guide table 3-1)
    """
    opList = [ OpDesc(opClass='MemRead'),
               OpDesc(opClass='FloatMemRead'),
               OpDesc(opClass='MemWrite'),
               OpDesc(opClass='FloatMemWrite') ]
    count = 2

class O3_ARM_Neoverse_N1_PredAlu(FUDesc):
    opList = [ OpDesc(opClass='SimdPredAlu')  ]
    count = 1

class O3_ARM_Neoverse_N1_FUP(FUPool):
    FUList = [
        O3_ARM_Neoverse_N1_Simple_Int(),
        O3_ARM_Neoverse_N1_Complex_Int(),
        O3_ARM_Neoverse_N1_LoadStore(),
        O3_ARM_Neoverse_N1_PredAlu(),
        O3_ARM_Neoverse_N1_FP()
        ]


class O3_ARM_Neoverse_N1_BP(BiModeBP):
    """
    Bi-Mode Branch Predictor
    """
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 16
    instShiftAmt = 2

class NovoO3CPU(ArmO3CPU):
    """
    Sources for this configuration:
    (1) neoverse-wiki
    https://en.wikichip.org/wiki/arm_holdings/microarchitectures/neoverse_n1
    (2) https://developer.arm.com/documentation/swog309707/latest
    (3) The Arm Neoverse N1 Platform: Building Blocks for the
        Next-Gen Cloud-to-Edge Infrastructure SoC, white paper
    (4) https://chipsandcheese.com/2021/10/22/deep-diving-neoverse-n1/
    (5) https://github.com/aakahlow/gem5Valid_Haswell

    Latencies of L1 L2 and L3 cache were taken from (5)
    but modified to match those in (3) Also refer to
    https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9059267&tag=1
    why Icache has latencies 1
    Haswell latencies: L1 = 4 cyles, L2 = 12 cycles, L3 = 36 cycles
    Neo-n1  latencies: L1 = 4 cyles, L2 = 11 cycles, L3 = 28-33 cycles
    """
    def __init__(self):

        super().__init__()

        self.decodeToFetchDelay = 1
        self.renameToFetchDelay = 1
        self.iewToFetchDelay = 1
        self.commitToFetchDelay = 1
        self.renameToDecodeDelay = 1
        self.iewToDecodeDelay = 1
        self.commitToDecodeDelay = 1
        self.iewToRenameDelay = 1
        self.commitToIEWDelay = 1
        self.commitToRenameDelay = 1
        self.fetchWidth = 4 # taken from source 1.
        self.fetchBufferSize = 64
        self.fetchToDecodeDelay = 1
        self.decodeWidth = 4 # taken from source 1.
        self.decodeToRenameDelay = 1
        self.renameWidth = 8 # taken from (1)
        self.renameToIEWDelay = 1
        self.issueToExecuteDelay = 1
        self.dispatchWidth = 8
        self.issueWidth = 8 # taken from (1)
        self.wbWidth = 8
        self.iewToCommitDelay = 1
        self.renameToROBDelay = 1
        self.commitWidth = 8
        self.squashWidth = 8
        self.trapLatency = 13
        self.backComSize = 5
        self.forwardComSize = 5

        # taken from (1)
        self.numROBEntries = 128
        # taken from (4)
        self.numPhysFloatRegs = 128
        # taken from (4)
        self.numPhysVecRegs = 128
        # taken from (4)
        self.numPhysIntRegs = 120

        # taken from (1)
        self.numIQEntries = 120

        self.switched_out = False
        self.branchPred = O3_ARM_Neoverse_N1_BP()
        self.fuPool = O3_ARM_Neoverse_N1_FUP()

        self.LQEntries = 68 # taken from (1)
        self.SQEntries = 72 # taken from (1)
        self.LSQDepCheckShift = 0
        self.LFSTSize = 1024
        self.SSITSize = 1024