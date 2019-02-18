from .loader import Loader
import openml

class OpenMLLoader(Loader):

    def __init__(self, did):
        Loader.__init__(self, "OpenMLData")
        self.did = did

    def start_simulation(self, simulation):
        super().start_simulation(simulation)
        did = self.did
        dataset = openml.datasets.get_dataset(did)
        x, y = dataset.get_data(target=dataset.default_target_attribute)
        simulation.resources.dataset = openml.datasets.get_dataset(did)
        simulation.resources.data_x = x
        simulation.resources.data_y = y

    def outline_simulation(self, simulation, outline):
        super().outline_simulation(simulation, outline)

        if not outline.has_attribute("data", Dataset.Battle):
            outline.append_attribute("data", Dataset.Battle, [ Role.Configuration ], "Dataset")

    def load_divided(self, simulation):
        return (simulation.resources.data_x, simulation.resources.data_y)

    def record_member(self, member, record):
        """
        Record the state of a member
        """
        super().record_member(member, record)
        if not self.is_active(member):
            return None

        simulation = member.simulation
        record.data = simulation.resources.dataset.name
