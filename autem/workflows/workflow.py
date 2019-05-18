from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager
from ..simulation_settings import SimulationSettings

from ..scorers import MemberScoreQuery

import time

class Workflow(SimulationManager, SpecieManager, EpochManager):
    """
    Base class for workflows.

    Contains shared services and standard implementations for workflows.
    """

    def __init__(self) :
        SimulationManager.__init__(self)
        SpecieManager.__init__(self)
        EpochManager.__init__(self)

    ## Extensions

    def list_extensions(self):
        """
        Required override that lists the workflows extensions
        """
        raise NotImplementedError()

    def configure_extensions(self, simulation):
        """
        Configure any custom extensions to the simulations components
        """
        components = simulation.list_components()
        workflow_index = components.index(self)
        components[workflow_index+1:workflow_index+1] = self.list_extensions()
        simulation.set_components(components)

    ## Runtime

    def is_runtime_exceeded(self, container):
        duration = time.time() - container.get_simulation().get_start_time()
        max_time = SimulationSettings(container).get_max_time()
        runtime_exceeded = max_time is not None and duration >= max_time
        return runtime_exceeded

    def is_max_specie_reached(self, simulation):
        max_species = SimulationSettings(simulation).get_max_species()
        n_species = len(simulation.list_species())
        reached = max_species is not None and n_species >= max_species
        return reached

    def is_max_epochs_reached(self, specie):
        max_epochs = SimulationSettings(specie).get_max_epochs()
        n_epochs = len(specie.list_epochs())
        reached = max_epochs is not None and n_epochs >= max_epochs
        return reached

    def is_max_rounds_reached(self, epoch):
        max_rounds = SimulationSettings(epoch).get_max_rounds()
        n_rounds = epoch.get_round()
        reached = n_rounds >= max_rounds
        return reached

    ## Queries

    def has_epoch_progressed(self, epoch):

        prior_epoch = epoch.get_prior_epoch()
        if not prior_epoch:
            return (None, "First epoch")

        prior_top_member = prior_epoch.get_ranking().get_top_member()
        top_member = epoch.get_ranking().get_top_member()

        if not prior_top_member:
            return (None, "No prior top member")

        if not top_member:
            return (None, "No top member")

        prior_top_score_evaluation = MemberScoreQuery(prior_top_member)
        top_score_evaluation = MemberScoreQuery(top_member)

        score_progressed = top_score_evaluation.get_score() > prior_top_score_evaluation.get_score()
        if score_progressed:
            return (True, "Score improved")

        return (False, "No score progress")

    ## Workflow

    def configure_simulation(self, simulation):
        """
        Configure the simulation
        """
        self.configure_extensions(simulation)

    def is_simulation_finished(self, simulation):
        """
        Simulation finished if max time exceeded
        """
        if self.is_runtime_exceeded(simulation):
            return (True, "Max time")

        if self.is_max_specie_reached(simulation):
            return (True, "Max specie")

        return (False, None)

    def configure_specie(self, specie):
        pass

    def is_specie_finished(self, specie):
        """
        Specie finished
        """
        if self.is_runtime_exceeded(specie):
            return (True, "Max time")

        if self.is_max_epochs_reached(specie):
            return (True, "Max epochs")

        return (False, None)

    def configure_epoch(self, epoch):
        pass

    def is_epoch_finished(self, epoch):
        """
        Epoch finished
        """

        if self.is_runtime_exceeded(epoch):
            return (True, "Max time")

        if self.is_max_rounds_reached(epoch):
            return (True, "Max rounds")
        
        return (False, None)
