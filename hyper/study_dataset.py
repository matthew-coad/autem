from .container import Container

import os
import pandas

class StudyDataset(Container):

    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_study(self):
        return self.get_parent()

    def get_path(self):
        return self.get_study().get_path().joinpath(self.get_name())
    
    def get_outline_path(self):
        return self.get_path().joinpath("Outline.csv")

    def has_outline(self):
        return os.path.exists(self.get_outline_path())

    def get_results_path(self):
        return self.get_path().joinpath("Battle.csv")

    def has_results(self):
        return os.path.exists(self.get_results_path())

    def get_results(self):
        return pandas.read_csv(self.get_results_path(), header=0)

        