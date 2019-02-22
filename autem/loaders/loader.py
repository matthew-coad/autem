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

    def start_simulation(self, simulation):
        simulation.resources.loader = self
