from ..simulation_manager import SimulationManager

class Scorer(SimulationManager):

    def __init__(self, name, scoring):
        SimulationManager.__init__(self)
        self.name = name
        self.scoring = scoring

    def score(self, y_true, y_pred):
        raise NotImplementedError("Score function not defined")

    def configure_simulation(self, simulation):
        simulation.set_scorer(self)
