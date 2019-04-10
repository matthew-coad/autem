from .component import Component
from .ranking import Ranking

import time

from types import SimpleNamespace
import numpy as np

class Epoch:
    """
    Epoch of a simulation
    """
    def __init__(self, simulation, epoch_id): 
        self.simulation = simulation
        self.id = epoch_id

        self.event = None
        self.event_reason = None

        self.start_time = None
        self.end_time = None

        self.progressed = None
        self.ranking = None

        self.alive = None

    def prepare(self):
        """
        Prepare the epoch for execution
        """
        self.event = None
        self.event_reason = None

        self.alive = True
        self.start_time = time.time()        

    def progress(self, progressed, reason):
        """
        Notify the epoch that it progressed the simulation
        """
        # When a member gets a promotion its wonlost record is erased
        self.progressed = progressed
        self.event = "progress"
        self.event_reason = reason

    def ranked(self, ranking):
        """
        Notify the epoch of its member rankings
        """
        # When a member gets a promotion its wonlost record is erased
        self.ranking = ranking

    def finished(self):
        """
        Inform the epoch that it has finished
        """
        self.end_time = time.time()
        self.alive = False
