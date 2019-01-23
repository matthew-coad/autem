from . import components
from . import populations

import math
import datetime
import time

import numpy
from types import SimpleNamespace

class Simulation:
    """Simulation state"""
    def __init__(self, name, components, seed = 1234):
        self.name = name
        self.started = False
        self.complete = False
        self.components = components
        self.random_state = numpy.random.RandomState(seed)
        self.next_id = 1
        self.population = None

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def run(self, finalising = False):
        """
        Run one iteration of the simulation
        """
        self.started = True
        population = populations.Population(self, finalising, self.population)
        population.started_at = datetime.datetime.now()
        start_time = time.time()
        population.evaluate()
        population.battle()
        population.breed()
        population.duration = time.time() - start_time
        population.analyze()
        population.save()
        self.population = population
        self.complete = population.complete

