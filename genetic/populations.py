from .components import Component
from .members import Member

from types import SimpleNamespace
import numpy as np
import pandas as pd
import datetime

class Population:
    """Population that genetic algorithms act on"""

    def __init__(self, simulation, parent0 = None):
        self.id = simulation.generate_id()
        self.simulation = simulation
        if parent0 is None:
            self.generation = 1
        else:
            self.generation = parent0.generation + 1
        self.configuration = SimpleNamespace()
        self.evaluation = SimpleNamespace()
        self.members = []
        self.alive = []
        self.exhausted = []
        self.dead = []
        self.children = []
        self.started_at = None
        self.duration = None
        self.population_report = None
        self.member_report = None

        if parent0 is None:
            for component in simulation.components:
                component.initializePopulation(self)
        else:
            self.configuration = parent0.configuration
            survivors = parent0.alive + parent0.exhausted
            self.members = [Member(self, m) for m in survivors] + parent0.children

    def evaluate(self):
        """
        Evaluate the population
        """
        self.evaluation = SimpleNamespace()
        for component in self.simulation.components:
            component.evaluatePopulation(self)
        for member in self.members:
            member.evaluate()

    def compete(self):
        """
        Have members of the population compete to determine fitness
        """
        self.alive = self.members[:]
        self.exhausted = []
        self.dead = []
        for component in self.simulation.components:
            component.competePopulation(self)

    def breed(self):
        """
        Have members of the population breed to create children for the next generation
        """
        self.children = []
        for component in self.simulation.components:
            component.breedPopulation(self)

    def analyze(self):
        """
        Analyze the population
        """

        # Generate the member report
        member_rows = []
        for member in self.members:
            member_rows.append(member.report())
        member_report = self.getReportFrame(member_rows)

        # Generate the population  report
        row = SimpleNamespace()
        row.generation_prop = self.generation
        row.population_id = self.id
        if not self.started_at is None:
            row.started_at_prop = self.started_at.isoformat()
        else:
            row.started_at_prop = ""
        if not self.duration is None:
            row.duration_measure = self.duration
        else:
            row.duration_measure = 0
        row.alive_measure = len(self.alive)
        row.exhausted_measure = len(self.exhausted)
        row.dead_measure = len(self.dead)
        row.children_measure = len(self.children)
        
        for component in self.simulation.components:
            component.reportPopulation(self, row)
        population_rows = [row]
        population_report = self.getReportFrame(population_rows)

        # Update state
        self.population_report = population_report
        self.member_report = member_report

    def save(self):
        """
        Perform any saves
        """
        for component in self.simulation.components:
            component.savePopulation(self)

    def getReportColumns(self, rows):
        """
        Get all the columns for a report
        """
        columnDict = {}
        for row in rows:
            for k in row.__dict__:
                if not k in columnDict:
                    columnDict[k] = k
        return list(columnDict.keys())

    def getReportFrame(self, rows):
        """
        Convert a report into a data frame
        """
        columns = self.getReportColumns(rows)
        columnValues = dict([ (column, []) for column in columns ])
        for row in rows:
            for column in columns:
                value = getattr(row, column) if hasattr(row, column) else np.nan
                columnValues[column].append(value)
        frame = pd.DataFrame(data=columnValues) 
        return frame


class FixedPopulationSize(Component):

    def __init__(self, population_size):
        self.population_size = population_size

    def initializePopulation(self, population):
        population_size = self.population_size
        while (len(population.members) < population_size):
            member = Member(population)
            population.members.append(member)

    def breedPopulation(self, population):
        population_size = self.population_size
        random_state = population.simulation.random_state
        parents = population.alive + population.exhausted
        children_size = population_size - len(parents)
        while (len(population.children) < children_size):
            parent_indexes = random_state.choice(len(parents), 2, replace=False)
            child = Member(population, parents[parent_indexes[0]], parents[parent_indexes[1]])
            population.children.append(child)


