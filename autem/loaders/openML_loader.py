from .loader import Loader
from .dataset import Dataset
from ..reporters import DataType, Role
from ..simulation_manager import SimulationManager

import openml

from sklearn.model_selection import train_test_split
import pandas as pd

class OpenMLLoader(SimulationManager):

    def __init__(self, did):
        self._did = did

    def load_dataset(self, simulation):
        did = self._did
        openml_dataset = openml.datasets.get_dataset(did)
        x, y = openml_dataset.get_data(target=openml_dataset.default_target_attribute)
        feature_exclude = [ openml_dataset.default_target_attribute ]
        nominal_features = openml_dataset.get_features_by_type("nominal", exclude=feature_exclude)
        numeric_features = openml_dataset.get_features_by_type("numeric", exclude=feature_exclude)
        date_features = openml_dataset.get_features_by_type("date", exclude=feature_exclude)
        string_features = openml_dataset.get_features_by_type("string", exclude=feature_exclude)
        features = {
            "nominal": nominal_features,
            "numeric": numeric_features,
            "date": date_features,
            "string": string_features
        }

        dataset = Dataset(x,y,features)
        return dataset

    def configure_simulation(self, simulation):
        dataset = self.load_dataset(simulation)
        simulation.set_full_data(dataset)
