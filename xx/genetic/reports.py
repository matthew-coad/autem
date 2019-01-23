from .components import Component

import pandas as pd
import os
import fnmatch
import shutil

class SavePath(Component):
    """
    Population component that saves populations analysis to a path
    """
    def __init__(self, path):
        self.path = path

    def initializePopulation(self, population):
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def savePopulation(self, population):
        simulation = population.simulation

        population_filename = "%s_%05d.csv" % ("Population", population.generation)
        population_full_path = self.path.joinpath(population_filename)
        population_report = population.population_report
        population_report.to_csv(population_full_path, index=False)

        member_filename = "%s_%05d.csv" % ("Member", population.generation)
        member_full_path = self.path.joinpath(member_filename)
        member_report = population.member_report
        member_report.to_csv(member_full_path, index=False)

