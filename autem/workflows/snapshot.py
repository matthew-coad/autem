from .workflow import Workflow

import time

class Snapshot(Workflow):
    """
    The snapshow workflow produces a very quick snapshot simulation that runs one specie with no tuning
    """

    def __init__(self, max_time = None) :
        Workflow.__init__(self, max_time = max_time)

    # Extensions

    def list_extensions(self, simulation):
        """
        List extensions component needed by the workflow.
        These components are added to the master component list,
        """
        return self.list_standard_extensions()

    # Simulations

    def configure_simulation(self, simulation):
        """
        Configure the simulation
        """
        pass

    def is_simulation_finished(self, simulation):
        """
        Is the simulation finished.
        Value is the first component that returns a Non-Null value
        """
        return (True, "Reached max species")

    # Species

    def configure_specie(self, specie):
        specie.set_max_league(self.get_max_league())
        specie.set_mode("spotcheck")
        specie.set_max_reincarnations(self.get_max_reincarnations())
        specie.set_max_population(self.get_max_population())

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        return (True, "Reached max epochs")
