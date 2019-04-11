from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation, get_score_evaluation

import numpy as np
from scipy import stats

class EpochProgressJudge(Evaluater):
    """
    Component that judges if a epoch has progressed the simulation
    """

    def judge_epoch(self, epoch):

        specie = epoch.get_specie()
        if epoch.id == 1:
            # First epoch
            # Indicate that it progressed
            epoch.progress(True, "First epoch")
            return None

        prior_epoch_id = epoch.id - 1
        prior_epoch = specie.get_epoch(prior_epoch_id)

        prior_top_member = prior_epoch.get_ranking().top_member()
        top_member = epoch.get_ranking().top_member()

        if not prior_top_member:
            epoch.progress(True, "Ranking progressed")
            return None

        if not top_member:
            epoch.progress(True, "No top member")
            return None            

        prior_top_score_evaluation = get_score_evaluation(prior_top_member)
        top_score_evaluation = get_score_evaluation(prior_top_member)

        score_progressed = top_score_evaluation.score > prior_top_score_evaluation.score

        if score_progressed:
            epoch.progress(True, "Score improved")
            return None

        epoch.progress(False, "No progress")
