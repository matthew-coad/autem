from .loader import Loader

from ..reporting import Dataset, Role

import openml

from sklearn.model_selection import train_test_split
import pandas as pd

class OpenMLLoaderState:

    def __init__(self):
        self.dataset = None
        self.features = None
        self.x_divided = None
        self.y_divided = None

        self.x_train = None
        self.x_validation = None
        self.y_train = None
        self.y_validation = None


class OpenMLLoader(Loader):

    def __init__(self, did, validation_size = 0.2):
        self.did = did
        self.validation_size = validation_size

    def prepare_simulation(self, simulation):
        super().prepare_simulation(simulation)

        random_state = simulation.get_random_state()
        validation_size = self.validation_size
        did = self.did
        dataset = openml.datasets.get_dataset(did)
        x, y = dataset.get_data(target=dataset.default_target_attribute)
        feature_exclude = [ dataset.default_target_attribute ]
        nominal_features = dataset.get_features_by_type("nominal", exclude=feature_exclude)
        numeric_features = dataset.get_features_by_type("numeric", exclude=feature_exclude)
        date_features = dataset.get_features_by_type("date", exclude=feature_exclude)
        string_features = dataset.get_features_by_type("string", exclude=feature_exclude)
        features = {
            "nominal": nominal_features,
            "numeric": numeric_features,
            "date": date_features,
            "string": string_features
        }

        if not validation_size is None:
            x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, random_state=random_state)
        else:
            x_train, x_validation, y_train, y_validation = (x, None, y, None)

        state = OpenMLLoaderState()

        state.dataset = dataset
        state.features = features
        state.x_divided = x
        state.y_divided = y

        state.x_train = x_train
        state.x_validation = x_validation
        state.y_train = y_train
        state.y_validation = y_validation

        simulation.set_state("openml_loader", state)

    def get_openml_loader_state(self, container):
        return container.get_simulation().get_state("openml_loader")

    def load_divided_data(self, container):
        state = self.get_openml_loader_state(container)
        return (state.x_divided, state.y_divided)

    def load_training_data(self, container):
        state = self.get_openml_loader_state(container)
        return (state.x_train, state.y_train)

    def load_validation_data(self, container):
        state = self.get_openml_loader_state(container)
        return (state.x_validation, state.y_validation)

    def get_features(self, container):
        state = self.get_openml_loader_state(container)
        return state.features

