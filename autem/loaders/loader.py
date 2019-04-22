from ..controller import Controller
from ..container import Container

class Loader(Controller):

    def start_simulation(self, simulation):
        simulation.set_state("loader", self)

    def load_divided_data(self, simulation):
        """
        Load data already divided into x,y arrays
        """
        raise NotImplementedError()
    
    def load_training_data(self, simulation):
        """
        Load training data
        """
        raise NotImplementedError()

    def load_validation_data(self, simulation):
        """
        Load validation data already divided into x,y arrays
        """
        raise NotImplementedError()

    def get_features(self, simulation):
        """
        Return dictionary of index of features by type
        """
        raise NotImplementedError()

class LoaderContainer:

    def get_loader(self):
        return self.get_simulation().get_state("loader")
