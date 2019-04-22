from ..controller import Controller
from ..container import Container

class Scorer(Controller):

    def __init__(self, name, scoring):
        self.name = name
        self.scoring = scoring

    def score(self, y_true, y_pred):
        raise NotImplementedError("Score function not defined")

    def start_simulation(self, simulation):
        simulation.set_state("scorer", self)

class ScorerContainer:

    def __init__(self):
        self._scorer = None

    def get_scorer(self):
        return self.get_simulation().get_state("scorer")
