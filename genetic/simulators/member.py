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
        self.form = None
        self.evaluations = []
        self.contests = []
        self.incarnation = None
        self.n_victory = 0
        self.n_defeat = 0
        self.dead = False

    """
    Notify this member that it has incarnated
    """
    def incarnated(self, form):
        self.form = form
        self.incarnation = form.count

    def contested(self, result):
        """
        Record a battle result
        """
        if result.victor_id() == self.id:
            self.n_victory += 1
        if result.loser_id() == self.id:
            self.n_defeat += 1
        self.contests.append(result)

    def killed(self):
        """
        Notify this member that is has been killed
        """
        self.dead = True

