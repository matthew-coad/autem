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
        self._decision_dict = dict((d.get_decision(), d) for d in decision_grid)
        self._initialized = True

    def get_decision_grid(self):
        """
        Get the decision grid
        """
        return self._decision_grid

    def get_initialized(self):
        """
        Has the decision grid been initialized
        """
        return self._initialized

    def introduce_decision(self, decision):
        """
        Track that a decision has been introduced to the simulation
        """
        self._decision_dict[decision].introduce()

    def get_decision_introductions(self, decision):
        return self._decision_dict[decision].get_introductions()

    def list_outstanding_decisions(self, max_introductions = 0):
        """
        List decisions that have yet to be introduced
        """
        decisions = [d.get_decision() for d in self.get_decision_grid() if d.get_introductions() <= max_introductions]
        return decisions

    def get(specie):
        return specie.get_state("DecisionGrid", lambda: DecisionGridState())
