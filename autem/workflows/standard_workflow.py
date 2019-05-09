from .workflow import Workflow

from .. import scorers
from .. import tuners

from .duration_evaluator import DurationEvaluator
from .diverse_contest import DiverseContest
from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from ..simulation_settings import SimulationSettings
from ..tuners import TuneSettings

import time

class StandardWorkflow(Workflow):
    """
    The standard workflow spotchecks until there is no more improvement, then tunes until their is no more improvement.
    """

    def __init__(self, max_epochs = None, max_species = 1) :
        self._max_epochs = max_epochs
        self._max_species = max_species

    def get_max_epochs(self):
        return self._max_epochs

    def get_max_species(self):
        return self._max_species

    # Simulations

    def list_extensions(self):
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

        super().configure_simulation(simulation)

        settings = SimulationSettings(simulation)
        settings.set_max_epochs(self._max_epochs)
        settings.set_max_species(self._max_species)

    # Species

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        epoch = specie.get_current_epoch()
        tuning = TuneSettings(epoch).get_tuning()

        progressed, reason = self.has_epoch_progressed(epoch)
        if progressed == False and tuning:
            return (True, reason)

        return super().is_specie_finished(specie)

    def configure_epoch(self, epoch):

        super().configure_epoch(epoch)

        tune_settings = TuneSettings(epoch)
        prior_epoch = epoch.get_prior_epoch()
        progressed, reason = self.has_epoch_progressed(prior_epoch) if prior_epoch else (None, None)
        prior_is_tuning = tune_settings.get_tuning() if prior_epoch else None
        tuning = True if (prior_epoch and prior_is_tuning) or progressed == False else None
        tune_settings.set_tuning(tuning)

