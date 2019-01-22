from .component import Component
from .battle_result import BattleOutcome

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
        self.n_victory = 0
        self.n_defeat = 0

    def matched(self, result):
        """
        Record that a member took place in a match
        """
        if result.is_victorious(self.id):
            self.n_victory += 1
        if result.is_defeated(self.id):
            self.n_defeat += 1



