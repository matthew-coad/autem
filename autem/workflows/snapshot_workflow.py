from .workflow import Workflow

from .. import scorers
from .. import tuners

from .duration_evaluator import DurationEvaluator
from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from ..simulation_settings import SimulationSettings

import time

class SnapshotWorkflow(Workflow):
    """
    The snapshow workflow produces a very quick snapshot simulation that runs one specie with no tuning
    """

    def __init__(self, max_epochs = 2) :
        Workflow.__init__(self)
        self._max_epochs = max_epochs

    # Simulations

    def list_extensions(self):
        extensions = [
            tuners.DecisionGridManager(),
            tuners.GPDecisionModel(),
            tuners.PrioritySpotcheck(),
            tuners.CrossoverSpotcheck(),
            tuners.CrossoverTuner(),

            scorers.ScoreContest(),
            DurationEvaluator(),
            
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

