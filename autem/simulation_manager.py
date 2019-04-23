class SimulationManager:

    ## Simulation managers

    def configure_simulation(self, simulation):
        """
        Configure a simulation
        """
        pass

    def prepare_simulation(self, simulation):
        """
        Prepare for the start of a simulation
        """
        pass

    def is_simulation_finished(self, simulation):
        """
        Is the simulation finished.
        Value is the first component that returns a Non-Null value
        """
        return (None, None)

    def finish_simulation(self, simulation):
        """
        Finish up the simulation. Perform final reporting, collect stats, etc.
        """
        pass

    def bury_simulation(self, simulation):
        """
        Bury any expensive resources allocated to the simulation
        """
        pass

class SimulationManagerContainer:

    def list_simulation_managers(self):
        managers = [c for c in self.list_components() if isinstance(c, SimulationManager) ]
        return managers
