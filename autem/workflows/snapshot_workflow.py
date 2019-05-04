from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager

from .. import scorers
from .. import tuners

from .duration_evaluator import DurationEvaluator
from .diverse_contest import DiverseContest
from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from ..simulation_settings import SimulationSettings

import time

class SnapshotWorkflow(SimulationManager, SpecieManager, EpochManager):
    """
    The snapshow workflow produces a very quick snapshot simulation that runs one specie with no tuning
    """

    def __init__(self, max_epochs = 2, max_time = None) :
        self._max_time = max_time
        self._max_epochs = max_epochs

    # Simulations

    def list_snapshot_extensions(self):
        extensions = [
            scorers.MemberScoreManager(),

            tuners.DecisionGridManager(),
            tuners.GPDecisionModel(),
            tuners.PrioritySpotcheck(),
            tuners.CrossoverSpotcheck(),
            tuners.CrossoverTuner(),

            DurationEvaluator(),
            DiverseContest(1.0),
            ContestJudge(),
            ScoreRater(),
        ]
        return extensions


    def configure_simulation(self, simulation):
        """
        Configure the simulation
        """
        components = simulation.list_components()
        snapshot_index = components.index(self)
        components[snapshot_index+1:snapshot_index+1] = self.list_snapshot_extensions()
        simulation.set_components(components)

        settings = SimulationSettings(simulation)
        settings.set_max_time(self._max_time)
        settings.set_max_epochs(self._max_epochs)

    def is_simulation_finished(self, simulation):
        """
        Is the simulation finished.
        Simulation is finished if any component elects to finish it
        """
        n_species = len(simulation.list_species())
        if n_species > 0:
            return (True, "Ran specie")
        return (False, None)

    # Species

    def configure_specie(self, specie):
        pass

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        epoch = specie.get_current_epoch()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())

        settings = SimulationSettings(specie)

        max_epochs = settings.get_max_epochs()
        max_time = settings.get_max_time()

        if n_epochs >= max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)

