from .loader import Loader

from ..simulators import Dataset
from ..simulators import Role

from sklearn.model_selection import train_test_split

class Data(Loader):
    
    def __init__(self, data_name, x, y, validation_size = 0.2):
        self.data_name = data_name
        self.x = x
        self.y = y
        self.validation_size = validation_size

    def outline_simulation(self, simulation, outline):
        super().outline_simulation(simulation, outline)

        if not outline.has_attribute("data", Dataset.Battle):
            outline.append_attribute("data", Dataset.Battle, [ Role.Configuration ], self.data_name)

    def start_simulation(self, simulation):
        super().start_simulation(simulation)

        random_state = simulation.random_state
        validation_size = self.validation_size
        x = self.x
        y = self.y
        x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, random_state=random_state)

        simulation.resources.x_train = x_train
        simulation.resources.x_validation = x_validation
        simulation.resources.y_train = y_train
        simulation.resources.y_validation = y_validation

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        super().record_member(member, record)
        record.data = self.data_name

    def load_divided_data(self, simulation):
        return (self.x, self.y)

    def load_training_data(self, simulation):
        return (simulation.resources.x_train, simulation.resources.y_train)

    def load_validation_data(self, simulation):
        return (simulation.resources.x_validation, simulation.resources.y_validation)
