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
        self.birth = 0
        self.incarnation = 0
        self.n_victory = 0
        self.n_defeat = 0
        self.dead = 0
        self.attractive = 0

    """
    Notify this member that an attempt is being made to incarnate
    """
    def incarnating(self):
        self.birth += 1

    """
    Notify this member that it has incarnated
    """
    def incarnated(self, form):
        self.form = form
        self.incarnation = form.count

    """
    Notify this member that it is considered "grown" to adult hood
    """
    def grown(self):
        self.birth = 0

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
        self.dead = 1

    def hubba(self):
        """
        Notify this member that it is attractive
        """
        self.attractive = 1
