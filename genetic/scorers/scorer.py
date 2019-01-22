from ..simulators import Component

class Scorer(Component):

    def score(self, y_true, y_pred):
        raise NotImplementedError("Score function not defined")

    def start_simulation(self, simulation):
        simulation.resources.scorer = self

