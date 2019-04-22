from ..lifecycle import LifecycleManager

class Scorer(LifecycleManager):

    def __init__(self, name, scoring):
        LifecycleManager.__init__(self)
        self.name = name
        self.scoring = scoring

    def score(self, y_true, y_pred):
        raise NotImplementedError("Score function not defined")

    def start_simulation(self, simulation):
        simulation.set_state("scorer", self)

class ScorerContainer:

    def get_scorer(self):
        return self.get_simulation().get_state("scorer")
