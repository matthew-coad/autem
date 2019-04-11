from .component import Component
from .ranking import Ranking

import time

from types import SimpleNamespace
import numpy as np

class Specie:
    """
    Specie of a simulation
    """
    def __init__(self, simulation, specie_id): 
        self.simulation = simulation
        self.id = specie_id

        self.event = None
        self.event_reason = None

        self.start_time = None
        self.end_time = None

        self.ranking = None
        self.alive = None
        self.resources = SimpleNamespace()

    def prepare(self):
        """
        Prepare the speie for execution
        """
        self.event = None
        self.event_reason = None

        self.alive = True
        self.start_time = time.time()        

    def finished(self):
        """
        Inform the specie that it has finished
        """
        self.end_time = time.time()
        self.alive = False
