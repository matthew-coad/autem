from ..simulation_manager import SimulationManager

class Hyperlearner(SimulationManager):

    def __init__(self):
        SimulationManager.__init__(self)

    def list_components(self):
        """
        Required override that lists the hyperlearners components
        """
        raise NotImplementedError()

    def configure_simulation(self, simulation):
        components = simulation.list_components()
        additional_components = self.list_components()
        hyper_index = components.index(self)
        components[hyper_index+1:hyper_index+1] = additional_components
        simulation.set_components(components)
