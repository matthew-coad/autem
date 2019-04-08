from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation, get_score_evaluation
from .stability_contest_evaluation import StabilityContestEvaluation, get_stability_contest_evaluation

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class StabilityContest(Evaluater):
    """
    Seeks to improve model stability by having contests on score variation
    """

    def contest_members(self, contestant1, contestant2, outcome):

        simulation = contestant1.simulation

        contestant1.evaluation.stability_contest_evaluation = StabilityContestEvaluation()
        contestant2.evaluation.stability_contest_evaluation = StabilityContestEvaluation()

        contestant1_score_eval = get_score_evaluation(contestant1)
        contestant2_score_eval = get_score_evaluation(contestant2)

        # Must have a range of scores to have a stability contest
        if contestant1_score_eval.score_std is None or contestant2_score_eval.score_std is None:
            return None

        # Must have difference scores to have a stability contest
        if contestant1_score_eval.score_std  == contestant2_score_eval.score_std:
            return None

        if contestant1_score_eval.score_std < contestant2_score_eval.score_std:
            # Contestant 1 is the winner
            contestant1.victory()
            get_stability_contest_evaluation(contestant1).stability_contest = "Victory"
            contestant2.defeat()
            get_stability_contest_evaluation(contestant2).stability_contest = "Defeat"
            
        else:
            # Contestant 2 is the winner
            contestant1.defeat()
            get_stability_contest_evaluation(contestant1).stability_contest = "Defeat"
            contestant2.victory()
            get_stability_contest_evaluation(contestant2).stability_contest = "Victory"

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = get_stability_contest_evaluation(member)
        record.SC_outcome = evaluation.stability_contest
