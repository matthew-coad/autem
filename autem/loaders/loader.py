from ..simulation_manager import SimulationManager

class Loader(SimulationManager):

    def configure_simulation(self, simulation):
        simulation.set_loader(self)

    def load_divided_data(self, container):
        """
        Load data already divided into x,y arrays
        """
        raise NotImplementedError()
    
    def load_training_data(self, container):
        """
        Load training data
        """
        raise NotImplementedError()

    def load_validation_data(self, container):
        """
        Load validation data already divided into x,y arrays
        """
        raise NotImplementedError()

    def get_features(self, container):
        """
        Return dictionary of index of features by type
        """
        raise NotImplementedError()
