from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager

from .score_evaluator import ScoreEvaluator
from .choice_evaluator import ChoiceEvaluator
from .duration_evaluator import DurationEvaluator

from .score_contest import ScoreContest
from .diverse_contest import DiverseContest

from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from .cross_over_maker import CrossoverMaker
from .top_choice_maker import TopChoiceMaker

import time

class Snapshot(SimulationManager, SpecieManager, EpochManager):
    """
    The snapshow workflow produces a very quick snapshot simulation that runs one specie with no tuning
    """

    def __init__(self, max_epochs = 2, max_time = None) :
        self._max_time = max_time
        self._max_epochs = max_epochs

    def get_max_time(self):
        return self._max_time

    def get_max_rounds(self):
        return 20

    def get_max_league(self):
        return 4

    def get_max_population(self):
        return 20

    def get_max_reincarnations(self):
        return 3

    def get_max_epochs(self):
        return self._max_epochs

    # Simulations

    def list_snapshot_extensions(self):
        extensions = [
            ScoreEvaluator(),
            ChoiceEvaluator(),
            DurationEvaluator(),

            ScoreContest(),
            DiverseContest(1.0),

            TopChoiceMaker(),
            CrossoverMaker(),

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
        specie.set_max_league(self.get_max_league())
        specie.set_max_reincarnations(self.get_max_reincarnations())
        specie.set_max_population(self.get_max_population())

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        epoch = specie.get_current_epoch()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if n_epochs >= max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)

    def configure_epoch(self, epoch):
        """
        Configure the epoch
        Value is the first component that returns a Non-Null value
        """
        epoch.set_max_rounds(self.get_max_rounds())

    def is_epoch_finished(self, epoch):
        return (False, None)



