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
        self.dead = False

    def contested(self, result):
        """
        Record a battle result
        """
        if result.victor_id() == self.id:
            self.n_victory += 1
        if result.loser_id() == self.id:
            self.n_defeat += 1
        if result.loser_id() == self.id and result.is_fatal():
            self.dead = True
        self.contests.append(result)

