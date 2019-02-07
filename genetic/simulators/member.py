from .component import Component
from .outcome import OutcomeType

from types import SimpleNamespace
import numpy as np

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

        self.preparations = SimpleNamespace()
        self.ready = 0

        self.evaluation = SimpleNamespace()

        self.accuracies = []
        self.accuracy = None

        self.maturity = None
        self.mature = 0

        self.contests = 0
        self.standoffs = 0
        self.victories = 0
        self.defeats = 0
        self.wonlost = []

        self.robustness = None
        self.fatality = 0
        self.attractiveness = None
        self.attractive = 0

        self.rating = None
        self.rating_sd = None

        self.ranking = None

    def incarnated(self, form, incarnation):
        """
        Notify this member that it has incarnated
        """
        if self.alive == 1:
            raise RuntimeError("Member already incarnated")
        self.form = form
        self.incarnation = incarnation
        self.alive = 1

    def prepared(self):
        """
        Notify this member that it has been prepared
        """
        self.ready = 1

    def accuracy_measured(self, accuracy):
        """
        Notify this member that its accuracy was measured
        """
        self.accuracies.append(accuracy)
        self.accuracy = np.array(self.accuracies).mean()

    def _contested(self):
        self.attractiveness = None
        self.robustness = None

    def stand_off(self):
        """
        Record a stand off
        """
        self._contested()
        self.contests += 1
        self.standoffs += 1

    def honour(self):
        """
        Record a victory
        """
        self._contested()
        self.contests += 1
        self.victories += 1
        self.wonlost.append(1)

    def chastise(self):
        self._contested()
        self.contests += 1
        self.defeats += 1 
        self.wonlost.append(0)

    def maturing(self, maturity, mature):
        """
        Notify member that it is maturing
        """
        if self.mature == 0:
            self.mature = mature
        self.maturity = maturity

    def checked_out(self, attractiveness, attractive):
        """
        Notify member that its being checked out to determine its attractiveness
        """
        if self.attractive == 0:
            self.attractive = attractive
        self.attractiveness = attractiveness

    def stressed(self, robustness, fatality):
        """
        Notify member that its being stressed
        """
        if self.fatality == 0:
            self.fatality = fatality
        self.robustness = robustness

    def rate(self, rating, rating_sd):
        self.rating = rating
        self.rating_sd = rating_sd

    def rank(self, ranking):
        self.ranking = ranking

    def failed(self, fault):
        """
        Notify this member that is has failed due to an error
        """
        self.fault = fault        

    def killed(self, cause_death):
        """
        Notify this member that is has been killed
        """
        if not self.cause_death is None:
            raise RuntimeError("Member already killed")
        if self.alive == 0:
            raise RuntimeError("Member not alive")
        self.alive = 0
        self.cause_death = cause_death
