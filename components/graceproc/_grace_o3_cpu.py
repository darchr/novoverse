from m5.objects import (
    ArmO3CPU,
    FUDesc,
    OpDesc,
    FUPool,
)

from m5.objects.FUPool import *

from m5.objects.BranchPredictor import BiModeBP, SimpleBTB


class O3_ARM_Grace_FP_Vec_0(FUDesc):
    """
    This class refers to FP/ASIMD 0/1 (symbol V in (2) table 3)
    Copied from Neoverse V1 optimization guide,
    latency taken for specific instruction in brackets
    """

    # ASIMD arithmetic basis (add & sub)
    opList = [
        # FP arith (fadd)-3.12
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP compare (fccmpe)-3.12
        OpDesc(opClass="FloatCmp", opLat=2),
        # Fp (vfma)-3.12
        OpDesc(opClass="FloatMultAcc", opLat=4),
        # Fp convert (vcvt)-3.13
        OpDesc(opClass="FloatCvt", opLat=3),
        # Vec arith basis (add)-3.16
        OpDesc(opClass="SimdAdd", opLat=2),
        # Vec logical (and)  -3.16
        OpDesc(opClass="SimdAlu", opLat=2),
        # Vec compare (cmeq) -3.16
        OpDesc(opClass="SimdCmp", opLat=2),
        # miscelleaneaus
        OpDesc(opClass="FloatMisc", opLat=3),
        # (vadd) -3.17
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        # Vec (vmla)-3.17
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        # Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        # SVE FP Red f64 (fmaxv)
        OpDesc(opClass="SimdFloatReduceCmp", opLat=3),
        # Fp multiply (fmul)-3.12
        OpDesc(opClass="FloatMult", opLat=3),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAes", opLat=2),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAesMix", opLat=2),
        # Vec integer multiply(mul)-3.16
        OpDesc(opClass="SimdMult", opLat=4),
        # Vec move, immed (vmov) -3.16
        OpDesc(opClass="SimdMisc", opLat=2),
        # SVE reduction (saddv)-3.16
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        # SVE reduction, logical (andv)
        OpDesc(opClass="SimdReduceAlu", opLat=3),
        # SVE FP associative add (fadda)
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        # PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass="SimdPredAlu", opLat=2),
        # V02 and V01
        # Fp divide (vdiv)- average latency-3.13
        OpDesc(opClass="FloatDiv", opLat=11, pipelined=False),
        # Vec FP divide f64 (fdiv)- we take average latency-3.17
        OpDesc(opClass="SimdFloatDiv", opLat=11, pipelined=False),
        # Fp square root D-form (fsqrt)- average latency-3.13
        OpDesc(opClass="FloatSqrt", opLat=12, pipelined=False),
        # Vec reciprocal estimate (vrsqrte)
        OpDesc(opClass="SimdSqrt", opLat=9),
        # Vec FP square root f64 (vsqrt)- we take average latency-3.17
        OpDesc(opClass="SimdFloatSqrt", opLat=12, pipelined=False),
        # Vec multiply accumulate, D-form (mla) -3.16
        OpDesc(opClass="SimdMultAcc", opLat=4),
        # Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass="SimdCvt", opLat=3),
        # V0
        # Crypto SHA1 hash acceleration op(sha1h) - 2 latency -3.22
        OpDesc(opClass="SimdSha1Hash2", opLat=2),
        # Crypto SHA1 hash acceleration ops (SHA1M)-3.22
        OpDesc(opClass="SimdSha1Hash", opLat=4),
        # Crypto SHA1 schedule acceleration ops (SHA1SU0)-3.22
        OpDesc(opClass="SimdShaSigma3", opLat=2),
        # Crypto SHA256 hash acceleration ops (SHA256H) -3.22
        OpDesc(opClass="SimdSha256Hash", opLat=4),
        # Crypto SHA256 hash acceleration ops (SHA256H2)-3.22
        OpDesc(opClass="SimdSha256Hash2", opLat=4),
        # Crypto SHA256 schedule acceleration ops(sha256su0)-3.22
        OpDesc(opClass="SimdShaSigma2", opLat=2),
        # Crypto SHA256 schedule acceleration ops(sha256su1)-3.22
        OpDesc(opClass="SimdShaSigma3", opLat=2),
    ]

    count = 1


class O3_ARM_Grace_FP_Vec_1(FUDesc):
    opList = [
        # Common V
        # FP arith (fadd)-3.12
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP compare (fccmpe)-3.12
        OpDesc(opClass="FloatCmp", opLat=2),
        # Fp (vfma)-3.12
        OpDesc(opClass="FloatMultAcc", opLat=4),
        # Fp convert (vcvt)-3.13
        OpDesc(opClass="FloatCvt", opLat=3),
        # Vec arith basis (add)-3.16
        OpDesc(opClass="SimdAdd", opLat=2),
        # Vec logical (and)  -3.16
        OpDesc(opClass="SimdAlu", opLat=2),
        # Vec compare (cmeq) -3.16
        OpDesc(opClass="SimdCmp", opLat=2),
        # miscelleaneaus
        OpDesc(opClass="FloatMisc", opLat=3),
        # (vadd) -3.17
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        # Vec (vmla)-3.17
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        # Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        # SVE FP Red f64 (fmaxv)
        OpDesc(opClass="SimdFloatReduceCmp", opLat=3),
        # Fp multiply (fmul)-3.12
        OpDesc(opClass="FloatMult", opLat=3),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAes", opLat=2),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAesMix", opLat=2),
        # Vec integer multiply(mul)-3.16
        OpDesc(opClass="SimdMult", opLat=4),
        # Vec move, immed (vmov) -3.16
        OpDesc(opClass="SimdMisc", opLat=2),
        # SVE reduction (saddv)-3.16
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        # SVE reduction, logical (andv)
        OpDesc(opClass="SimdReduceAlu", opLat=3),
        # SVE FP associative add (fadda)
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        # PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass="SimdPredAlu", opLat=2),
        # V1
        # Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass="SimdCvt", opLat=3),
        # PREDALU has instructions in V1 group ( COMPACT), EOR
        OpDesc(opClass="SimdPredAlu", opLat=3),
        # V13
        # SVE reduction, arith, S form (smaxv)-3.16
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        # Vec absolute diff accum (vaba) -3.16
        OpDesc(opClass="SimdAddAcc", opLat=4),
        # Vec shift by immed, (shl)-3.16
        OpDesc(opClass="SimdShift", opLat=2),
        # Vec shift accumulate (vsra)-3.16
        OpDesc(opClass="SimdShiftAcc", opLat=4),
    ]
    count = 1


class O3_ARM_Grace_FP_Vec_2(FUDesc):
    opList = [
        # FP arith (fadd)-3.12
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP compare (fccmpe)-3.12
        OpDesc(opClass="FloatCmp", opLat=2),
        # Fp (vfma)-3.12
        OpDesc(opClass="FloatMultAcc", opLat=4),
        # Fp convert (vcvt)-3.13
        OpDesc(opClass="FloatCvt", opLat=3),
        # Vec arith basis (add)-3.16
        OpDesc(opClass="SimdAdd", opLat=2),
        # Vec logical (and)  -3.16
        OpDesc(opClass="SimdAlu", opLat=2),
        # Vec compare (cmeq) -3.16
        OpDesc(opClass="SimdCmp", opLat=2),
        # miscelleaneaus
        OpDesc(opClass="FloatMisc", opLat=3),
        # (vadd) -3.17
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        # Vec (vmla)-3.17
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        # Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        # SVE FP Red f64 (fmaxv)
        OpDesc(opClass="SimdFloatReduceCmp", opLat=3),
        # Fp multiply (fmul)-3.12
        OpDesc(opClass="FloatMult", opLat=3),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAes", opLat=2),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAesMix", opLat=2),
        # Vec integer multiply(mul)-3.16
        OpDesc(opClass="SimdMult", opLat=4),
        # Vec move, immed (vmov) -3.16
        OpDesc(opClass="SimdMisc", opLat=2),
        # SVE reduction (saddv)-3.16
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        # SVE reduction, logical (andv)
        OpDesc(opClass="SimdReduceAlu", opLat=3),
        # SVE FP associative add (fadda)
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        # PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass="SimdPredAlu", opLat=2),
        # Fp divide (vdiv)- average latency-3.13
        OpDesc(opClass="FloatDiv", opLat=11, pipelined=False),
        # Vec FP divide f64 (fdiv)- we take average latency-3.17
        OpDesc(opClass="SimdFloatDiv", opLat=11, pipelined=False),
        # Fp square root D-form (fsqrt)- average latency-3.13
        OpDesc(opClass="FloatSqrt", opLat=12, pipelined=False),
        # Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass="SimdCvt", opLat=3),
        # Vec multiply accumulate, D-form (mla) -3.16
        OpDesc(opClass="SimdMultAcc", opLat=4),
        # Vec reciprocal estimate (vrsqrte)
        OpDesc(opClass="SimdSqrt", opLat=9),
        # Vec FP square root f64 (vsqrt)- we take average latency-3.17
        OpDesc(opClass="SimdFloatSqrt", opLat=12, pipelined=False),
    ]
    count = 1


class O3_ARM_Grace_FP_Vec_3(FUDesc):
    opList = [
        # Common V
        # FP arith (fadd)-3.12
        OpDesc(opClass="FloatAdd", opLat=2),
        # FP compare (fccmpe)-3.12
        OpDesc(opClass="FloatCmp", opLat=2),
        # Fp (vfma)-3.12
        OpDesc(opClass="FloatMultAcc", opLat=4),
        # Fp convert (vcvt)-3.13
        OpDesc(opClass="FloatCvt", opLat=3),
        # Vec arith basis (add)-3.16
        OpDesc(opClass="SimdAdd", opLat=2),
        # Vec logical (and)  -3.16
        OpDesc(opClass="SimdAlu", opLat=2),
        # Vec compare (cmeq) -3.16
        OpDesc(opClass="SimdCmp", opLat=2),
        # miscelleaneaus
        OpDesc(opClass="FloatMisc", opLat=3),
        # (vadd) -3.17
        OpDesc(opClass="SimdFloatAdd", opLat=2),
        # Vec (vmla)-3.17
        OpDesc(opClass="SimdFloatMultAcc", opLat=4),
        # Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass="SimdFloatCmp", opLat=2),
        # SVE FP Red f64 (fmaxv)
        OpDesc(opClass="SimdFloatReduceCmp", opLat=3),
        # Fp multiply (fmul)-3.12
        OpDesc(opClass="FloatMult", opLat=3),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAes", opLat=2),
        # Fp multiply (fmul)-3.22
        OpDesc(opClass="SimdAesMix", opLat=2),
        # Vec integer multiply(mul)-3.16
        OpDesc(opClass="SimdMult", opLat=4),
        # Vec move, immed (vmov) -3.16
        OpDesc(opClass="SimdMisc", opLat=2),
        # SVE reduction (saddv)-3.16
        OpDesc(opClass="SimdReduceAdd", opLat=2),
        # SVE reduction, logical (andv)
        OpDesc(opClass="SimdReduceAlu", opLat=3),
        # SVE FP associative add (fadda)
        OpDesc(opClass="SimdFloatReduceAdd", opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass="SimdFloatMisc", opLat=2),
        # PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass="SimdPredAlu", opLat=2),
        # V13
        # SVE reduction, arith, S form (smaxv)-3.16
        OpDesc(opClass="SimdReduceCmp", opLat=2),
        # Vec absolute diff accum (vaba) -3.16
        OpDesc(opClass="SimdAddAcc", opLat=4),
        # Vec shift by immed, (shl)-3.16
        OpDesc(opClass="SimdShift", opLat=2),
        # Vec shift accumulate (vsra)-3.16
        OpDesc(opClass="SimdShiftAcc", opLat=4),
    ]
    count = 1


class O3_ARM_Grace_Simple_Int(FUDesc):
    """
    This class refers to pipelines Branch0, Integer single Cycles 0,
    Integer single Cycle 1 (symbol B and S in (2) table 3)
    """

    # Aarch64 ALU (Unfortunately branches are put together with IntALU)
    opList = [OpDesc(opClass="IntAlu", opLat=1)]
    count = 6


class O3_ARM_Grace_Complex_Int(FUDesc):
    """
    This class refers to pipelines integer single/multicycle 1
    (this refers to pipeline symbol M in (2) table 3)
    """

    # Aarch64 Int ALU
    opList = [
        OpDesc(opClass="IntAlu", opLat=1),  #  Int ALU
        OpDesc(opClass="IntMult", opLat=2),  #  Int mult
        # Int divide W-form (sdiv)- we take average
        OpDesc(opClass="IntDiv", opLat=5, pipelined=False),
        OpDesc(opClass="IprAccess", opLat=1),  #  Prefetch
        # Latency varies alot for different instructions in this group.
        OpDesc(opClass="SimdPredAlu"),
    ]
    count = 2


class O3_ARM_Grace_LoadStore(FUDesc):
    """
    This class refers to Load/Store0/1
    (symbol L in Neoverse guide table 3-1)
    """

    opList = [
        OpDesc(opClass="MemRead"),
        OpDesc(opClass="FloatMemRead"),
        OpDesc(opClass="MemWrite"),
        OpDesc(opClass="FloatMemWrite"),
    ]
    count = 2


class O3_ARM_Grace_Load(FUDesc):
    opList = [OpDesc(opClass="MemRead"), OpDesc(opClass="FloatMemRead")]
    count = 1


class O3_ARM_Grace_Store(FUDesc):
    opList = [OpDesc(opClass="MemWrite"), OpDesc(opClass="FloatMemWrite")]
    count = 2


class O3_ARM_Grace_FUP(FUPool):
    FUList = [
        O3_ARM_Grace_FP_Vec_0(),
        O3_ARM_Grace_FP_Vec_1(),
        O3_ARM_Grace_FP_Vec_2(),
        O3_ARM_Grace_FP_Vec_3(),
        O3_ARM_Grace_Simple_Int(),  # 6
        O3_ARM_Grace_Complex_Int(),  # 2
        O3_ARM_Grace_LoadStore(),  #
        O3_ARM_Grace_Load(),
        O3_ARM_Grace_Store(),
    ]


class O3_ARM_Grace_BP(BiModeBP):
    """
    Bi-Mode Branch Predictor
    """

    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    btb = SimpleBTB(numEntries=4096, tagBits=18)
    RASSize = 16
    instShiftAmt = 2


class GraceO3CPU(ArmO3CPU):
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

        self.commitToIEWDelay = 1
        self.commitToRenameDelay = 1
        self.iewToRenameDelay = 1
        self.commitToDecodeDelay = 1
        self.iewToDecodeDelay = 1
        self.renameToDecodeDelay = 1
        self.commitToFetchDelay = 1
        self.iewToFetchDelay = 1
        self.renameToFetchDelay = 1
        self.decodeToFetchDelay = 1
        self.fetchWidth = 8
        self.fetchBufferSize = 64
        self.fetchToDecodeDelay = 1
        self.decodeWidth = 8
        self.decodeToRenameDelay = 1
        self.renameWidth = 8
        self.renameToIEWDelay = 1
        self.issueToExecuteDelay = 1
        self.dispatchWidth = 8
        self.issueWidth = 8
        self.wbWidth = 8
        self.iewToCommitDelay = 1
        self.renameToROBDelay = 1
        self.commitWidth = 8
        self.squashWidth = 8
        self.trapLatency = 13
        self.backComSize = 5
        self.forwardComSize = 5

        self.numROBEntries = 320
        self.numPhysFloatRegs = 192
        self.numPhysVecRegs = 192
        self.numPhysIntRegs = 224

        self.numIQEntries = 120

        # self.cacheStorePorts = 512
        # self.cacheLoadPorts = 512

        self.switched_out = False
        self.branchPred = O3_ARM_Grace_BP()
        self.fuPool = O3_ARM_Grace_FUP()

        self.LQEntries = 68
        self.SQEntries = 72
        self.LSQDepCheckShift = 0
        self.LFSTSize = 1024
        self.SSITSize = 1024
