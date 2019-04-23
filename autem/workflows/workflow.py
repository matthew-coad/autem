from ..simulation_manager import SimulationManager
from ..evaluators import ScoreEvaluator, ChoiceEvaluator, ValidationEvaluator, DurationEvaluator
from ..evaluators import ScoreContest, DiverseContest
from ..evaluators import ContestJudge, EpochProgressJudge
from ..evaluators import ScoreRater
from ..makers import TopChoiceMaker, CrossoverMaker, TuneMaker

import time

class Workflow(SimulationManager):
    """
    Base class for simulation workflow controllers.

    Workflows are responsible for controlling the overall progress of a simulation. They are responsible for deciding on what type of specie/epoch will
    be created, how many and whether the simulation should be terminated
    """

    def __init__(self, max_time = None):
        self._max_time = max_time

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

    def list_standard_extensions(self):
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
            EpochProgressJudge(),
           
            ScoreRater(),
        ]
        return extensions

    # Species

    def configure_specie(self, specie):
        """
        Configure the epoch
        Value is the first component that returns a Non-Null value
        """
        raise NotImplementedError()

    def is_specie_finished(self, specie):
        """
        Is the specie finished.
        Value is the first component that returns a Non-Null value
        """
        raise NotImplementedError()

    # Epochs

    def configure_epoch(self, epoch):
        """
        Configure the epoch
        Value is the first component that returns a Non-Null value
        """
        epoch.set_max_rounds(self.get_max_rounds())

    def is_epoch_finished(self, epoch):
        """
        Is the epoch finished.
        Value is the first component that returns a Non-Null value
        """
        max_time = self.get_max_time()
        duration = time.time() - epoch.get_simulation().get_start_time()

        if max_time is not None and duration >= max_time:
            return (True, "Max time")
        
        return (False, None)

