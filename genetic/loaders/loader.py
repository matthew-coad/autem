from ..simulators import Component

class Loader(Component):
    
    def load_divided(self, simulation):
        """
        Load data already divided into x,y arrays
        """
        pass

    def start_simulation(self, simulation):
        simulation.resources.loader = self
