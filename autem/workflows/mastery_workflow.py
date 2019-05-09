from .workflow import Workflow

from .. import scorers
from .. import tuners

from .duration_evaluator import DurationEvaluator
from .diverse_contest import DiverseContest
from .contest_judge import ContestJudge
from .score_rater import ScoreRater

from ..tuners import TuneSettings

from ..choice import Choice

import time

class MasteryWorkflow(Workflow):
    """
    The mastery process runs a spotcheck to determine target workflows then switches
    to tuning mode to get better performance from the targetted workflows
    """

    def __init__(self, spotcheck_epochs = 3) :
        self._spotcheck_epochs = spotcheck_epochs
    
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

    # Species

    def is_specie_finished(self, specie):
        epoch = specie.get_current_epoch()
        tuning = TuneSettings(epoch).get_tuning()

        progressed, reason = self.has_epoch_progressed(epoch)
        if progressed == False and tuning:
            return (True, reason)

        return super().is_specie_finished(specie)

    # Epoch

    def configure_epoch(self, epoch):
        super().configure_epoch(epoch)

        epoch_n = epoch.get_epoch_n() 
        spotcheck_epochs = self._spotcheck_epochs
        tuning = epoch_n > spotcheck_epochs
        tune_settings = TuneSettings(epoch)
        tune_settings.set_tuning(tuning)
        tune_settings.set_spotchecking(not tuning)
