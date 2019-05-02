from ..specie import Specie

class DecisionModelState:

    def __init__(self, specie):
        assert isinstance(specie, Specie)
        self._specie = specie

    def get_decision_model(self):
        return self._specie.get_state("decision_model")

    def set_decision_model(self, model):
        return self._specie.set_state("decision_model",model)

    def get(specie):
        return DecisionModelState(specie)