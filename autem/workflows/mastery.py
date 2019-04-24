from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager

from ..evaluators import ScoreEvaluator, ChoiceEvaluator, ValidationEvaluator, DurationEvaluator
from ..evaluators import ScoreContest, DiverseContest
from ..evaluators import ContestJudge, EpochProgressJudge
from ..evaluators import ScoreRater

from .cross_over_maker import CrossoverMaker
from .top_choice_maker import TopChoiceMaker
from .tune_maker import TuneMaker


import time

class Mastery(SimulationManager, SpecieManager, EpochManager):
    """
    The mastery workflow follows the machine learning master workflow
    """

    def __init__(self, max_time = None, max_spotchecks  = 3, max_tunes = 1, max_epochs = 20):
        Workflow.__init__(max_time=max_time)
        self._max_spotchecks = max_spotchecks
        self._max_tunes = max_tunes
        self._max_epochs = max_epochs

    # Properties

    def get_max_epochs(self):
        return self._max_epochs

    def get_max_spotchecks(self):
        return self._max_spotchecks

    def get_max_tunes(self):
        return self._max_tunes

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

        duration = time.time() - self.get_start_time()
        specie = self.get_current_specie()

        max_spotchecks = self.get_max_spotchecks()
        n_spotchecks = len(self.list_species(mode = "spotcheck" ))

        max_tunes = self.get_max_tunes()
        n_tunes = len(self.list_species(mode = "tune" ))

        if n_spotchecks + n_tunes >= max_spotchecks + max_tunes:
            return (True, "Reached max species")

        max_time = self.get_max_time()
        if max_time is not None and duration >= max_time:
            return (True, "Reached max time")
        
        return (False, None)

    # Species

    def is_specie_finished(self, specie):
        """
        Should we finish the species?
        """
        epoch = specie.get_current_epoch()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if not epoch.get_progressed():
            return (True, "No progress")

        if n_epochs == max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)

    def configure_specie(self, specie):
        specie.set_max_league(self.get_max_league())
        n_specie = specie.get_specie_n()
        mode = "spotcheck" if n_specie < self.get_max_spotchecks() else "tune"
        specie.set_mode("spotcheck")
        specie.set_max_league(self.get_max_league())
        specie.set_max_reincarnations(self.get_max_reincarnations())
        specie.set_max_population(self.get_max_population())


