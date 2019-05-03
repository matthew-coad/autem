from ..specie import Specie

class DecisionModelState:

    def __init__(self):
        self.reset()

    def get_decision_model(self):
        """
        Get decision score
        """
        return self._decision_model

    def get_evaluated(self):
        return self._evaluated

    def evaluated(self, decision_model):
        """
        Set the state as evaluated
        """
        self._decision_model = decision_model
        self._evaluated = True

    def reset(self):
        """
        Reset the state.
        """
        self._evaluated = False
        self._decision_model = None

    def get(specie):
        return DecisionModelState(specie)

    def get(specie):
        """
        Get decision state for a member
        """
        assert isinstance(specie, Specie)
        return specie.get_state("member_model", lambda: DecisionModelState())
