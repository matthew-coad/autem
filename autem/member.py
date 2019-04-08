from .component import Component

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
        self.initial_mutation_index = None

        self.event = "initialized"

        self.alive = 0
        self.kill_reason = None
        self.incarnation = 0
        self.final = 0

        self.resources = None

        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

        self.evaluation = SimpleNamespace()
        self.evaluations = 0
        self.evaluation_time = None
        self.evaluation_duration = None

        self.contests = 0
        self.victories = 0
        self.defeats = 0
        self.wonlost = []
        self.league = 0

        self.ratings = SimpleNamespace()
        self.rating = None
        self.rating_sd = None

        self.ranking = None

    def prepare(self):
        """
        Prepare this member for incarnation
        """
        self.resources = SimpleNamespace()
        self.fault = None
        self.fault_operation = None
        self.fault_component = None
        self.fault_message = None

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

    def evaluating(self):
        self.event = "evaluate"
        self.evaluation_time = time.time()
        self.evaluations += 1

    def evaluated(self, duration):
        self.evaluation_duration = duration

    def victory(self):
        """
        Record a victory
        """
        self.event = "victory"
        self.contests += 1
        self.victories += 1
        self.wonlost.append(1)

    def defeat(self):
        """
        Record a defeat
        """
        self.event = "defeat"
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
        if league is None:
            self.league += 1
        else:
            self.league = league
        self.victories = 0
        self.defeats = 0
        self.eliminations = 0
        self.contests = 0
        self.wonlost = []

    def kill(self, reason):
        """
        Kill this member
        """
        self.event = "death"
        self.alive = 0
        self.kill_reason = reason
        self.final = 1

    def fail(self, fault, operation, component):
        """
        Inform this member that it has failed for some reason
        """
        self.event = "fail"
        self.fault = fault
        self.fault_operation = operation
        self.fault_component = component
        self.fault_message = "%s %s - %s" % (operation, str(component), str(fault))
        self.alive = 0
        self.kill_reason = str(fault)
        self.final = 1

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
        self.event = "final"
        self.alive = 0
        self.final = 1
