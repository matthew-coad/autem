from .scorer import Scorer

class LeagueScorer(Scorer):

    def __init__(self, metric, splits):
        Scorer.__init__(self, metric, splits)
        


