from ..specie import Specie

class DecisionGridState:

    """
    State for a decision grid
    """

    def __init__(self):
        self._decision_grid = None
        self._initialized = False

    def initialize(self, decision_grid):
        """
        Initialize the decision grid
        """
        self._decision_grid = decision_grid
        self._initialized = True

    def get_decision_grid(self):
        return self._decision_grid

    def get_initialized(self):
        return self._initialized

    def get(specie):
        return specie.get_state("DecisionGrid", lambda: DecisionGridState())
