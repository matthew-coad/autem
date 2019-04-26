from ..simulation_manager import SimulationManager
from ..specie_manager import SpecieManager
from ..epoch_manager import EpochManager

from ..evaluators import ScoreEvaluator, ChoiceEvaluator, ValidationEvaluator, DurationEvaluator
from ..evaluators import ScoreContest, DiverseContest
from ..evaluators import ContestJudge
from ..evaluators import ScoreRater

from .cross_over_maker import CrossoverMaker
from .top_choice_maker import TopChoiceMaker
from .tune_maker import TuneMaker, TuneState, get_tune_state

import time

class Standard(SimulationManager, SpecieManager, EpochManager):
    """
    The standard workflow spotchecks until there is no more improvement, then tunes until their is no more improvement.
    """

    def __init__(self, max_time = None, max_epochs = None, max_species = None) :
        self._max_time = max_time
        self._max_epochs = max_epochs
        self._max_species = max_species

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

    def get_max_species(self):
        return self._max_species

    # Simulations

    def list_snapshot_extensions(self):
        extensions = [
            ScoreEvaluator(),
            ChoiceEvaluator(),
            ValidationEvaluator(),
            DurationEvaluator(),

            ScoreContest(),
            DiverseContest(1.0),

            TopChoiceMaker(),
            CrossoverMaker(),
            TuneMaker(),

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
        Finish the simulation once we have completed one species
        """
        n_species = len(simulation.list_species())
        max_species = self.get_max_species() if not self.get_max_species() is None else 1
        if n_species >= max_species:
            return (True, "Reached max species")
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
        is_tuning = epoch.is_tuning()
        duration = time.time() - specie.get_simulation().get_start_time()
        n_epochs = len(specie.list_epochs())
        max_epochs = self.get_max_epochs()
        max_time = self.get_max_time()

        if not max_epochs is None and n_epochs >= max_epochs:
            return (True, "Max epochs")

        if max_time is not None and duration >= max_time:
            return (True, "Max time")

        progressed, reason = self.has_epoch_progressed(epoch)
        if progressed == False and is_tuning:
            return (True, reason)
        
        return (False, None)

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

        prior_top_score_evaluation = prior_top_member.get_score_state()
        top_score_evaluation = top_member.get_score_state()

        score_progressed = top_score_evaluation.score > prior_top_score_evaluation.score
        if score_progressed:
            return (True, "Score improved")

        return (False, "No score progress")

    def configure_epoch(self, epoch):
        prior_epoch = epoch.get_prior_epoch()
        progressed, reason = self.has_epoch_progressed(prior_epoch) if prior_epoch else (None, None)
        mode = "tune" if (prior_epoch and prior_epoch.is_tuning()) or progressed == False else "spotcheck"

        epoch.set_max_rounds(self.get_max_rounds())
        epoch.set_mode(mode)

    def is_epoch_finished(self, epoch):
        return (False, None)



