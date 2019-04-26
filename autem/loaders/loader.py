from ..simulation_manager import SimulationManager

class Loader(SimulationManager):

    def configure_simulation(self, simulation):
        dataset = self.load_dataset(simulation)
        simulation.set_training_data(dataset)

    def load_dataset(self, simulation):
        """
        Load data and return as a dataset
        """
        raise NotImplementedError()

