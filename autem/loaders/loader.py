from .. import Controller

class Loader(Controller):

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

    def start_simulation(self, simulation):
        simulation.get_resources().loader = self
