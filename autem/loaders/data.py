from .loader import Loader
from ..reporting import Dataset, Role

from sklearn.model_selection import train_test_split
import pandas as pd

class DataState:

    def __init__(self):
        self.x_train = None
        self.x_validation = None
        self.y_train = None
        self.y_validation = None

class Data(Loader):
    
    def __init__(self, data_name, y, numeric_x = None, nominal_x = None, validation_size = 0.2):
        self.data_name = data_name
        self.y = y
        self.numeric_x = numeric_x
        self.nominal_x = nominal_x
        self.validation_size = validation_size

        x = None
        numeric_cols = 0
        nominal_cols = 0
        if not self.numeric_x is None:
            numeric_cols = self.numeric_x.shape[1]
            x = self.numeric_x
        
        if not self.nominal_x is None:
            nominal_cols = self.nominal_x.shape[1]
            if x is None:
                x = self.nominal_x
            else:
                x = pd.concat([x, self.nominal_x], axis=1)

        features = {
            "numeric": range(numeric_cols),
            "nominal": range(numeric_cols, numeric_cols + nominal_cols),
            "date": [],
            "string": []
        }
        self.x = x
        self.features = features

    def outline_simulation(self, simulation, outline):
        super().outline_simulation(simulation, outline)

        if not outline.has_attribute("data", Dataset.Battle):
            outline.append_attribute("data", Dataset.Battle, [ Role.Configuration ], self.data_name)

    def prepare_simulation(self, simulation):
        super().prepare_simulation(simulation)

        random_state = simulation.random_state
        validation_size = self.validation_size
        y = self.y
        x = self.x

        x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, random_state=random_state)

        state = DataState()
        state.x_train = x_train
        state.x_validation = x_validation
        state.y_train = y_train
        state.y_validation = y_validation
        simulation.set_state("data", state)

    def load_divided_data(self, container):
        return (self.x, self.y)

    def load_training_data(self, container):
        state = container.get_simulation().get_state("data")
        return (state.x_train, state.y_train)

    def load_validation_data(self, container):
        state = container.get_simulation().get_state("data")
        return (state.x_validation, state.y_validation)

    def get_features(self, container):
        return self.features

