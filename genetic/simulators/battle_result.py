from enum import Enum

class BattleOutcome(Enum):
    NoContest = 0,
    Inconclusive = 1,
    Indecisive = 2,
    Decisive = 3

class BattleResult:

    def __init__(self, member1_id, member2_id):
        self.member1_id = member1_id
        self.member2_id = member2_id
        self.outcome = BattleOutcome.NoContest
        self.victor = None

    def inconclusive(self):
        self.outcome = BattleOutcome.Inconclusive
        self.victor = None

    def decisive(self, victor):
        self.outcome = BattleOutcome.Decisive
        self.victor = victor

    def is_victorious(self, member_id):
        """
        Was the given member victorious?
        """
        if self.outcome != BattleOutcome.Indecisive and self.outcome != BattleOutcome.Decisive:
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
        if self.outcome != BattleOutcome.Indecisive and self.outcome != BattleOutcome.Decisive:
            return False
        if self.member1_id == member_id and self.victor == 2:
            return True
        if self.member2_id == member_id and self.victor == 1:
            return True
        return False

