from enum import Enum
from types import SimpleNamespace

class OutcomeType(Enum):
    NoContest = 0,
    Inconclusive = 1,
    Indecisive = 2,
    Decisive = 3

class Outcome(SimpleNamespace):

    def __init__(self, member1_id, member2_id):
        self.member1_id = member1_id
        self.member2_id = member2_id
        self.type = OutcomeType.NoContest
        self.victor = None
        self.fatality = False

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

    def is_uncontested(self):
        return self.type == OutcomeType.NoContest

    def is_conclusive(self):
        return self.type != OutcomeType.NoContest and self.type != OutcomeType.Inconclusive

    def is_inconclusive(self):
        return self.type == OutcomeType.Inconclusive

    def is_victorious(self, member_id):
        """
        Was the given member victorious?
        """
        if self.type != OutcomeType.Indecisive and self.type != OutcomeType.Decisive:
            return False
        if self.member1_id == member_id and self.victor == 1:
            return True
        if self.member2_id == member_id and self.victor == 2:
            return True
        return False

    def is_defeated(self, member_id):
        """
        Was the given member defeated?
        """
        if self.type != OutcomeType.Indecisive and self.type != OutcomeType.Decisive:
            return False
        if self.member1_id == member_id and self.victor == 2:
            return True
        if self.member2_id == member_id and self.victor == 1:
            return True
        return False



