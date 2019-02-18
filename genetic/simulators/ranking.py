from enum import Enum
from types import SimpleNamespace

class RankingType(Enum):
    NoContest = 0,
    Inconclusive = 1,
    Conclusive = 1

class Ranking(SimpleNamespace):

    def __init__(self, step):
        self.step = step
        self.type = RankingType.NoContest
        self.members = []

    def inconclusive(self):
        self.type = RankingType.Inconclusive

    def conclusive(self, members):
        """
        Indecisive contest outcome.
        """
        self.type = RankingType.Conclusive
        self.members = members

    def is_uncontested(self):
        return self.type == RankingType.NoContest

    def is_conclusive(self):
        return self.type == RankingType.Conclusive

    def is_inconclusive(self):
        return self.type == RankingType.Inconclusive

