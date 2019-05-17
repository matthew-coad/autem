from .scorer import Scorer

class LeagueScorer(Scorer):

    def __init__(self, metric, n_splits = 5):
        Scorer.__init__(self, metric, n_splits)
        


