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
        self.final = 0

        self.event = "initialized"
        self.event_time = None

        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        self.resources = SimpleNamespace()
        self.starts = 0

        self.evaluation = SimpleNamespace()

        self.contests = 0
        self.evaluations = 0
        self.standoffs = 0
        self.victories = 0
        self.defeats = 0
        self.eliminations = 0
        self.wonlost = []
        self.league = 0

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
        self.event = "evaluated"
        self.event_time = time.time()
        self.evaluations += 1

    def stand_off(self):
        """
        Record a stand off
        """
        self.contests += 1
        self.standoffs += 1
        self.event = "standoff"
        self.event_time = time.time()

    def victory(self):
        """
        Record a victory
        """
        self.event = "victory"
        self.event_time = time.time()
        self.contests += 1
        self.victories += 1
        self.wonlost.append(1)

    def defeat(self):
        """
        Record a defeat
        """
        self.event = "defeat"
        self.event_time = time.time()
        self.contests += 1
        self.defeats += 1 
        self.wonlost.append(0)

    def promote(self, league = None):
        """
        Promote the member to the next league
        """
        # When a member gets a promotion it wonlost record is erased
        # From now on only contests at the higher league level will count
        self.event = "promotion"
        self.event_time = time.time()
        if league is None:
            self.league += 1
        else:
            self.league = league
        self.victories = 0
        self.defeats = 0
        self.eliminations = 0
        self.contests = 0
        self.wonlost = []

    def eliminate(self):
        """
        Eliminate this member
        """
        self.event = "eliminate"
        self.event_time = time.time()
        self.alive = 0
        self.final = 1

    def eliminator(self):
        """
        Notify member that they eliminated another member
        """
        self.event = "eliminator"
        self.event_time = time.time()
        self.eliminations += 1

    def fail(self, fault, operation, component):
        """
        Fault this member
        """
        self.event = "fail"
        self.event_time = time.time()
        self.fault = fault
        self.fault_operation = operation
        self.fault_component = component
        self.fault_message = "%s %s - %s" % (operation, str(component), str(fault))
        self.alive = 0

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

    def finshed(self):
        """
        Notify that this member it is finished with, because the simulation has finished
        """
        if self.alive == 0:
            raise RuntimeError("Member not alive")
        self.event = "final"
        self.event_time = time.time()
        self.alive = 0
        self.final = 1
