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
        self.round = None

    def prepare(self):
        """
        Prepare the epoch for operation
        """
        self.event = None
        self.event_reason = None

        self.alive = True
        self.start_time = time.time()

        self.round = 0

    def prepare_round(self):
        """
        Prepare the epoch for its next round
        """
        self.round += 1

    def progress(self, progressed, reason):
        """
        Inform the epoch of its progress
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
        Epoch has finished
        """
        self.end_time = time.time()
        self.alive = False
