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
        self.round = None

        self.epoch = None
        self.contests = {} # Map of contests per epoch
        self.wonlost = {}  # Map of wonlost record per epoch

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

    def prepare_epoch(self, epoch):
        self.event = None
        self.epoch = epoch
        self.contests[self.epoch] = 0
        self.wonlost[self.epoch] = []
        self.round = None

    def prepare_evaluation(self, round):
        self.evaluation_time = time.time()
        self.round = round

    def evaluated(self, duration):
        self.evaluation_duration = duration
        self.evaluations += 1

    def victory(self):
        """
        Record a victory at a given step
        """
        self.contests[self.epoch] += 1
        self.wonlost[self.epoch].append(1)

    def defeat(self):
        """
        Record a defeat at a given epoch
        """
        self.contests[self.epoch] += 1
        self.wonlost[self.epoch].append(0)

    def promote(self, league = None):
        """
        Promote the member to the next league
        """
        # When a member gets a promotion its wonlost record is erased
        self.event = "promotion"
        if league is None:
            self.league += 1
        else:
            self.league = league

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
