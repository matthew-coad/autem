from ..simulators import Controller

class Scorer(Controller):

    def __init__(self, name, scoring):
        self.name = name
        self.scoring = scoring

    def score(self, y_true, y_pred):
        raise NotImplementedError("Score function not defined")

    def start_simulation(self, simulation):
        simulation.resources.scorer = self

