from .loader import Loader
from .. import Dataset, Role

import openml

from sklearn.model_selection import train_test_split

class OpenMLLoader(Loader):

    def __init__(self, did, validation_size = 0.2):
        self.did = did
        self.validation_size = validation_size

    def start_simulation(self, simulation):
        super().start_simulation(simulation)

        random_state = simulation.random_state
        validation_size = self.validation_size
        did = self.did
        dataset = openml.datasets.get_dataset(did)
        x, y = dataset.get_data(target=dataset.default_target_attribute)

        x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, random_state=random_state)

        simulation.resources.dataset = dataset
        simulation.resources.x_divided = x
        simulation.resources.y_divided = y

        simulation.resources.x_train = x_train
        simulation.resources.x_validation = x_validation
        simulation.resources.y_train = y_train
        simulation.resources.y_validation = y_validation

    def outline_simulation(self, simulation, outline):
        super().outline_simulation(simulation, outline)

        if not outline.has_attribute("data", Dataset.Battle):
            outline.append_attribute("data", Dataset.Battle, [ Role.Configuration ], "Dataset")

    def load_divided_data(self, simulation):
        return (simulation.resources.x_divided, simulation.resources.y_divided)

    def load_training_data(self, simulation):
        return (simulation.resources.x_train, simulation.resources.y_train)

    def load_validation_data(self, simulation):
        return (simulation.resources.x_validation, simulation.resources.y_validation)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        super().record_member(member, record)

        simulation = member.simulation
        record.data = simulation.resources.dataset.name
