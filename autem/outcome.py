from enum import Enum
from types import SimpleNamespace

class OutcomeType(Enum):
    NoContest = 0,
    Inconclusive = 1,
    Indecisive = 2,
    Decisive = 3,
    Unconventional = 4

class Outcome(SimpleNamespace):

    def __init__(self, step, member1_id, member2_id):
        self.step = step
        self.member1_id = member1_id
        self.member2_id = member2_id
        self.type = OutcomeType.NoContest
        self.victor = None

    def inconclusive(self):
        self.type = OutcomeType.Inconclusive
        self.victor = None

    def indecisive(self, victor):
        """
        Indecisive contest outcome.
        """
        self.type = OutcomeType.Indecisive
        self.victor = victor

    def decisive(self, victor):
        """
        Decisive contest outcome.
        """
        self.type = OutcomeType.Decisive
        self.victor = victor

    def unconventional(self):
        """
        Outcome is unconventional.
        A component knows what to do
        """
        self.type = OutcomeType.Unconventional
        self.victor = None

    def is_uncontested(self):
        return self.type == OutcomeType.NoContest

    def is_conclusive(self):
        return self.type == OutcomeType.Decisive or self.type == OutcomeType.Indecisive or self.type == OutcomeType.Unconventional

    def is_decisive(self):
        return self.type == OutcomeType.Decisive

    def is_indecisive(self):
        return self.type == OutcomeType.Indecisive

    def is_inconclusive(self):
        return self.type == OutcomeType.Inconclusive

    def is_unconventional(self):
        return self.type == OutcomeType.Mad

    def is_zero_sum(self):
        return self.type == OutcomeType.Decisive or self.type == OutcomeType.Indecisive

    def victor_id(self):
        if self.type != OutcomeType.Decisive and self.type != OutcomeType.Indecisive:
            return None
        victor_id = self.member1_id if self.victor == 1 else self.member2_id
        return victor_id

    def loser_id(self):
        if self.type != OutcomeType.Decisive and self.type != OutcomeType.Indecisive:
            return None
        loser_id = self.member2_id if self.victor == 1 else self.member1_id
        return loser_id
