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
        self.alive = 0
        self.incarnation = 0

        self.cause_death = None
        self.fault = None
        self.attractive = 0
        self.mature = 0

        self.evaluations = 0
        self.contests = 0
        self.victories = 0
        self.defeats = 0
        self.wonlost = []

        self.evaluation = None
        self.contest = None

    def incarnated(self, form, incarnation):
        """
        Notify this member that it has incarnated
        """
        if self.alive == 1:
            raise RuntimeError("Member already incarnated")
        self.form = form
        self.incarnation = incarnation
        self.alive = 1

    def evaluated(self, evaluation):
        """
        Notify this member that an evaluation was performed
        """
        self.evaluation = evaluation
        self.evaluations += 1

    def matured(self):
        """
        Notify member that it has matured into "Adulthood"
        """
        if self.mature == 0:
            self.mature = 1

    def hubbify(self):
        """
        Notify member that it is attractive
        """
        if self.attractive == 0:
            self.attractive = 1

    def contested(self, contest):
        """
        Record a battle result
        """
        self.contest = contest
    
    def honour(self):
        self.victories += 1
        self.wonlost.append(1)

    def chastise(self):
        self.defeats += 1 
        self.wonlost.append(0)

    def killed(self, cause_death, fault):
        """
        Notify this member that is has been killed
        """
        if not self.cause_death is None:
            raise RuntimeError("Member already killed")
        if self.alive == 0:
            raise RuntimeError("Member not alive")
        self.alive = 0
        self.cause_death = cause_death
        self.fault = fault
