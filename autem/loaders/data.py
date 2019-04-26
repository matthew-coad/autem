from .loader import Loader
from .dataset import Dataset
from ..simulation_manager import SimulationManager

from sklearn.model_selection import train_test_split
import pandas as pd

class Data(SimulationManager):
    
    def __init__(self, data_name, y, numeric_x = None, nominal_x = None):
        self.data_name = data_name

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

        dataset = Dataset(x, y, features)
        self._dataset = dataset

    def configure_simulation(self, simulation):
        simulation.set_full_data(self._dataset)

