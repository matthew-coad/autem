from ..lifecycle import LifecycleManager

class Loader(LifecycleManager):

    def start_simulation(self, simulation):
        simulation.set_state("loader", self)

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

class LoaderContainer:

    def get_loader(self):
        return self.get_simulation().get_state("loader")
