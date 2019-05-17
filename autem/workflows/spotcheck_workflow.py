from .workflow import Workflow

from .. import scorers
from .. import tuners

from .duration_evaluator import DurationEvaluator
from .diverse_contest import DiverseContest
from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from ..simulation_settings import SimulationSettings

import time

class SpotcheckWorkflow(Workflow):
    """
    The spotcheck workflow produces evaluated decisions without attempting to tune them
    """

    def __init__(self, max_epochs = 3) :
        Workflow.__init__(self)
        self._max_epochs = max_epochs

    # Simulations

    def list_extensions(self):
        extensions = [
            tuners.DecisionGridManager(),
            tuners.GPDecisionModel(),
            tuners.PrioritySpotcheck(),
            tuners.CrossoverSpotcheck(),

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

