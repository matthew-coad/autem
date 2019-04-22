from .evaluator import Evaluater

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class StabilityContestEvaluation:
    
    def __init__(self):
        self.stability_contest = None

def get_stability_contest_evaluation(member):
    """
     Get score contest evaluation for a member
    """
    evaluation = member.evaluation
    if not hasattr(evaluation, "stability_contest_evaluation"):
        evaluation.stability_contest_evaluation = StabilityContestEvaluation()
    return evaluation.stability_contest_evaluation


class StabilityContest(Evaluater):
    """
    Seeks to improve model stability by having contests on score variation
    """

    def contest_members(self, contestant1, contestant2):

        simulation = contestant1.simulation

        contestant1.evaluation.stability_contest_evaluation = StabilityContestEvaluation()
        contestant2.evaluation.stability_contest_evaluation = StabilityContestEvaluation()

        contestant1_score_eval = get_score_evaluation(contestant1)
        contestant2_score_eval = get_score_evaluation(contestant2)

        # Must have a range of scores to have a stability contest
        if contestant1_score_eval.score_std is None or contestant2_score_eval.score_std is None:
            return None

        def set_outcome(contestant, outcome):
            get_stability_contest_evaluation(contestant1).stability_contest = outcome

        # Must have difference scores to have a stability contest
        if contestant1_score_eval.score_std  == contestant2_score_eval.score_std:
            set_outcome(contestant1, "Draw")
            set_outcome(contestant2, "Draw")
            return None

        if contestant1_score_eval.score_std < contestant2_score_eval.score_std:
            # Contestant 1 is the winner
            contestant1.victory()
            set_outcome(contestant1, "Win")
            contestant2.defeat()
            set_outcome(contestant2, "Loss")
            
        else:
            # Contestant 2 is the winner
            contestant1.defeat()
            set_outcome(contestant1, "Loss")
            contestant2.victory()
            set_outcome(contestant2, "Win")

