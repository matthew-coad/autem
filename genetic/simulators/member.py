from .component import Component
from .outcome import OutcomeType

from types import SimpleNamespace

class Member:
    """
    Member of a population
    """
    def __init__(self, simulation): 
        self.simulation = simulation
        self.id = simulation.generate_id()
        self.configuration = SimpleNamespace()
        self.evaluations = []
        self.contests = []
        self.n_victory = 0
        self.n_defeat = 0

    def contested(self, result):
        """
        Record a battle result
        """
        if result.is_victorious(self.id):
            self.n_victory += 1
        if result.is_defeated(self.id):
            self.n_defeat += 1
        self.contests.append(result)

