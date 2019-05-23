from .container import Container
from .configuration_query import ConfigurationQuery
from .study_dataset import StudyDataset

import pandas

import os
from pathlib import Path

class Study(Container):

    def __init__(self, name):
        Container.__init__(self)
        self._name = name
        self._datasets = None

    def get_name(self):
        return self._name

    def get_hyper_analysis(self):
        return self.get_parent()

    def get_path(self):
        query = ConfigurationQuery(self.get_hyper_analysis())
        return query.get_hyper_simulations_path().joinpath(self.get_name())

    def get_datasets_status(self):
        """
        Returns a dataframe listing the status of each dataset for the study
        """
        path = self.get_path()
        directories = pandas.Series([ str(o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))], name= "directories")
        datasets = self.get_hyper_analysis().get_datasets_status()
        datasets['exists'] = datasets["name"].isin(directories)
        datasets['attempted'] = datasets['name'].map(lambda n: os.path.exists(path.joinpath(n).joinpath("Outline.csv")))
        datasets['results'] = datasets['name'].map(lambda n: os.path.exists(path.joinpath(n).joinpath("Battle.csv")))
        return datasets

    def _make_datasets(self):
        datasets_status = self.get_hyper_analysis().get_datasets_status()
        names = datasets_status['name'].tolist()
        datasets = [ StudyDataset(n) for n in names ]
        for dataset in datasets:
            dataset.set_parent(self)
        return datasets

    def get_datasets(self):
        if self._datasets == None:
            self._datasets = self._make_datasets()
        return self._datasets

    def get_dataset(self, name):
        return next((d for d in self.get_datasets() if d.get_name() == name), None)
