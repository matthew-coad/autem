from .component import Component
from .outcome import OutcomeType

import time

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

        self.event = "initialized"
        self.event_time = None
        self.fault = None

        self.resources = SimpleNamespace()
        self.starts = 0

        self.evaluation = SimpleNamespace()

        self.maturity = None
        self.mature = 0
        self.contests = 0
        self.evaluations = 0
        self.standoffs = 0
        self.victories = 0
        self.defeats = 0
        self.dominations = 0
        self.thrashings = 0
        self.wonlost = []

        self.robustness = None
        self.fatality = 0
        self.attractiveness = None
        self.attractive = 0

        self.ratings = SimpleNamespace()
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
        self.event = "birth"
        self.event_time = time.time()

    def started(self):
        """
        Notify this member that it has been started
        """
        if self.starts:
            raise RuntimeError("Member already started")
        self.starts += 1

    def evaluated(self):
        self.evaluations += 1

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
        self.event = "standoff"
        self.event_time = time.time()

    def victory(self, decisive):
        """
        Record a victory
        """
        self._contested()
        self.contests += 1
        self.victories += 1
        if decisive:
            self.dominations += 1
            self.event = "domination"
        else:
            self.event = "victory"
        self.event_time = time.time()
        self.wonlost.append(1)

    def defeat(self, decisive):
        self._contested()
        self.contests += 1
        self.defeats += 1 
        if decisive:
            self.thrashings += 1
            self.event = "thrashing"
        else:
            self.event = "defeat"
        self.event_time = time.time()
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
        Notify member that its being checked out to determine its fame
        """
        if self.attractive == 0 and attractive == 1:
            self.event = "inducted"
            self.event_time = time.time()
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

    def rated(self, rating, rating_sd):
        """
        Set the members rating in the hall of fame
        """
        self.rating = rating
        self.rating_sd = rating_sd

    def ranked(self, ranking):
        """
        Set the members ranking in the hall of fame
        """
        self.ranking = ranking

    def faulted(self, fault):
        """
        Notify this member that is has a fault
        """
        self.event = "fault"
        self.event_time = time.time()
        self.fault = fault
        self.alive = 0

    def killed(self):
        """
        Notify this member that is has been killed
        """
        self.event = "death"
        self.event_time = time.time()
        self.alive = 0

    def finshed(self):
        """
        Notify that this member it is finished with, because the simulation has finished
        """
        if self.alive == 0:
            raise RuntimeError("Member not alive")
        self.event = "final"
        self.event_time = time.time()
        self.alive = 0