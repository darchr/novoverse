
from m5.objects import ArmO3CPU
from m5.objects.BranchPredictor import (
    TournamentBP,
)

class NovoO3CPU(ArmO3CPU):
    def __init__(self):
        """
        """
        super().__init__()
        self.fetchWidth = 8
        self.decodeWidth = 8
        self.renameWidth = 8
        self.issueWidth = 8
        self.wbWidth = 8
        self.commitWidth = 8

        self.numROBEntries = 192

        self.numPhysIntRegs = 128
        self.numPhysFloatRegs = 128

        self.branchPred = TournamentBP()

        self.LQEntries = 128
        self.SQEntries = 128
