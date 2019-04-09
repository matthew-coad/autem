from .. import Dataset, Role, WarningInterceptor
from .evaluator import Evaluater
from .score_evaluation import ScoreEvaluation, get_score_evaluation

import numpy as np
from scipy import stats

from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline

import time
import warnings

import logging
import io

class ScoreContest(Evaluater):
    """
    Determines fitness by comparing model scores 
    """

    def contest_members(self, contestant1, contestant2):

        simulation = contestant1.simulation
        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        contestant1_score = get_score_evaluation(contestant1).score
        contestant2_score = get_score_evaluation(contestant2).score

        if contestant1_score == contestant2_score and contestant1.id < contestant2.id:
            victor = 1
        elif contestant1_score == contestant2_score and contestant1.id > contestant2.id:
            victor = 2
        elif contestant1_score > contestant2_score:
            victor = 1
        elif contestant1_score < contestant2_score:
            victor = 2
        else:
            raise RuntimeError("Victory condition not found")

        winner = contestant1 if victor == 1 else contestant2
        loser = contestant2 if victor == 1 else contestant1

        winner.evaluation.accuracy_contest = "Win"
        winner.victory()
        loser.evaluation.accuracy_contest = "Loss"
        loser.defeat()

        if winner.league == 0 and loser.league > 0:
            winner.evaluation.accuracy_contest = "Upset Win"
            loser.evaluation.accuracy_contest = "Upset Loss"
            winner.promote()

    def record_member(self, member, record):
        super().record_member(member, record)

        evaluation = member.evaluation
        if hasattr(evaluation, "accuracy_contest"):
            record.accuracy_contest = evaluation.accuracy_contest
        else:
            record.accuracy_contest = None
