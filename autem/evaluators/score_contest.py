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

        specie = contestant1.get_specie()
        contestant1.evaluation.accuracy_contest = None
        contestant2.evaluation.accuracy_contest = None

        contestant1_score = get_score_evaluation(contestant1).score
        contestant2_score = get_score_evaluation(contestant2).score

        if contestant1_score == contestant2_score:
            contestant1.evaluation.accuracy_contest = "Draw"
            contestant2.evaluation.accuracy_contest = "Draw"
            return None

        if contestant1_score > contestant2_score:
            winner = contestant1
            loser = contestant2
        else:
            loser = contestant1
            winner = contestant2

        winner.evaluation.accuracy_contest = "Win"
        winner.victory()
        loser.evaluation.accuracy_contest = "Loss"
        loser.defeat()

